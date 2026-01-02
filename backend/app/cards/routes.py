from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .schemas import (
    CardCreate, CardUpdate, CardOut, CardMove,
    LabelCreate, LabelOut, SubtaskCreate, SubtaskUpdate, SubtaskOut
)
from ..auth.utils import get_current_user, get_db
from ..boards.models import Card, Board, List, User, Label, Subtask

router = APIRouter(prefix="/cards", tags=["cards"])

"""Módulo de endpoints para la gestión de 'cards' (tarjetas).

Contiene rutas para crear, listar, obtener, actualizar y eliminar tarjetas.
Cada endpoint valida que el tablero (board) pertenezca al usuario autenticado
antes de realizar operaciones que afecten a los recursos.
"""


def verify_board_permission(board_id: int, user_id: int, db: Session):
    """
    Verifica que el tablero existe y pertenece al usuario.
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")

    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")

    return board


# ================================== CREAR CARDS ==========================================
@router.post("/", response_model=CardOut)
def create_card(
    data: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea una nueva tarjeta (card) en un tablero y lista especificados.
    """

    verify_board_permission(data.board_id, current_user.id, db)

    new_card = Card(
        board_id=data.board_id,
        list_id=data.list_id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        created_by_id=current_user.id,
        updated_at=datetime.now(timezone.utc),
    )

    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card


@router.get("/", response_model=list[CardOut])
def get_cards(
    board_id: int,
    search: str = None,
    responsible_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_board_permission(board_id, current_user.id, db)

    query = db.query(Card).filter(Card.board_id == board_id)

    if search:
        query = query.filter(Card.title.ilike(f"%{search}%"))
    
    if responsible_id:
        query = query.filter(Card.responsible_id == responsible_id)

    return query.order_by(Card.list_id, Card.position).all()


# ============================ GET /cards/{card_id} ======================================
# ✅ CAMBIO 2: Rehabilitamos el endpoint que tus tests esperan (antes estaba comentado)
@router.get("/{card_id}", response_model=CardOut)
def get_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene una tarjeta por ID (si pertenece a un board del usuario).
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)
    return card


# ============================ PATCH /cards/{card_id} =====================================
# ✅ CAMBIO 3: Tus tests usan PATCH para editar. Lo añadimos para evitar 405.
@router.patch("/{card_id}", response_model=CardOut)
def update_card_patch(
    card_id: int,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Edita una tarjeta existente (PATCH).
    - Solo aplica los campos que vienen en el body.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)

    if data.title is not None:
        card.title = data.title
    if data.description is not None:
        card.description = data.description
    if data.due_date is not None:
        card.due_date = data.due_date
    if data.list_id is not None:
        card.list_id = data.list_id

    card.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(card)
    return card


# ================================= ACTUALIZAR CARDS (PUT) =================================
# (lo dejamos para compatibilidad, pero los tests usan PATCH)
@router.put("/{card_id}", response_model=CardOut)
def update_card_put(
    card_id: int,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Edita una tarjeta existente (PUT).
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)

    if data.title is not None:
        card.title = data.title
    if data.description is not None:
        card.description = data.description
    if data.due_date is not None:
        card.due_date = data.due_date
    if data.list_id is not None:
        card.list_id = data.list_id

    card.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(card)
    return card


# ============================= MOVER CARDS ========================================
@router.patch("/{card_id}/move", response_model=CardOut)
def move_card(
    card_id: int,
    data: CardMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mueve una tarjeta entre columnas o dentro de la misma columna (Drag & Drop).

    El backend es la autoridad del orden:
    - valida permisos
    - normaliza posiciones
    - evita duplicados y huecos
    """

    # 1️⃣ La tarjeta debe existir
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    # 2️⃣ Seguridad
    verify_board_permission(card.board_id, current_user.id, db)

    # ✅ CAMBIO 4: Definimos primero old/new para que no reviente con UnboundLocalError
    old_list_id = card.list_id
    new_list_id = data.list_id
    new_order = data.order

    # ✅ CAMBIO 5: Validación correcta de "lista destino": consultamos List (no Card)
    list_dest = (
        db.query(List)
        .filter(List.id == new_list_id, List.board_id == card.board_id)
        .first()
    )
    if not list_dest:
        raise HTTPException(status_code=400, detail="Lista destino inválida")

    # 3️⃣ Obtener tarjetas destino (para límites)
    target_cards = (
        db.query(Card)
        .filter(Card.board_id == card.board_id, Card.list_id == new_list_id)
        .order_by(Card.position)
        .all()
    )

    # ✅ CAMBIO 6: Normalizamos new_order para evitar índices raros
    if new_order < 0:
        new_order = 0
    if new_order > len(target_cards):
        new_order = len(target_cards)

    # ================= CASO A: misma columna =================
    if old_list_id == new_list_id:
        # quitamos la card de la lista actual y la reinsertamos en new_order
        remaining = [c for c in target_cards if c.id != card.id]
        if new_order > len(remaining):
            new_order = len(remaining)
        remaining.insert(new_order, card)

        for idx, c in enumerate(remaining):
            c.position = idx
            c.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(card)
        return card

    # ================= CASO B: columna distinta =================

    # Reordenar columna origen (sin la card movida)
    source_cards = (
        db.query(Card)
        .filter(
            Card.board_id == card.board_id,
            Card.list_id == old_list_id,
            Card.id != card.id,
        )
        .order_by(Card.position)
        .all()
    )

    for idx, c in enumerate(source_cards):
        c.position = idx
        c.updated_at = datetime.now(timezone.utc)

    # Recalcular destino (antes de insertar)
    target_cards = (
        db.query(Card)
        .filter(Card.board_id == card.board_id, Card.list_id == new_list_id)
        .order_by(Card.position)
        .all()
    )

    if new_order > len(target_cards):
        new_order = len(target_cards)

    target_cards.insert(new_order, card)

    for idx, c in enumerate(target_cards):
        c.list_id = new_list_id
        c.position = idx
        c.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(card)
    return card


# ======================= DELETE CARDS ==============================================
@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina una tarjeta por ID si pertenece a un tablero del usuario autenticado.
    Retorna 204 si se elimina correctamente.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(card)
    db.commit()
    return None


# ======================= LABELS ==============================================

@router.post("/{card_id}/labels", response_model=LabelOut)
def add_label(
    card_id: int,
    data: LabelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)

    new_label = Label(card_id=card_id, name=data.name, color=data.color)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label

@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_label(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    
    card = db.query(Card).filter(Card.id == label.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(label)
    db.commit()
    return None


# ======================= SUBTASKS ==============================================

@router.post("/{card_id}/subtasks", response_model=SubtaskOut)
def add_subtask(
    card_id: int,
    data: SubtaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)

    # Get max position
    max_pos = db.query(Subtask).filter(Subtask.card_id == card_id).count()

    new_subtask = Subtask(card_id=card_id, title=data.title, position=max_pos)
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    return new_subtask

@router.patch("/subtasks/{subtask_id}", response_model=SubtaskOut)
def update_subtask(
    subtask_id: int,
    data: SubtaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtarea no encontrada")
    
    card = db.query(Card).filter(Card.id == subtask.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    if data.title is not None:
        subtask.title = data.title
    if data.completed is not None:
        subtask.completed = data.completed
    if data.position is not None:
        subtask.position = data.position

    db.commit()
    db.refresh(subtask)
    return subtask

@router.delete("/subtasks/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask(
    subtask_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtarea no encontrada")
    
    card = db.query(Card).filter(Card.id == subtask.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(subtask)
    db.commit()
    return None
