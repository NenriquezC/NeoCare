
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .schemas import CardCreate, CardUpdate, CardOut
from ..auth.utils import get_current_user, get_db
from ..boards.models import Card, Board, User

router = APIRouter(prefix="/cards", tags=["cards"])



def verify_board_permission(board_id: int, user_id: int, db: Session):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")

    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")

    return board



@router.post("/", response_model=CardOut)
def create_card(data: CardCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

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
def get_cards(board_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):

    verify_board_permission(board_id, current_user.id, db)

    return db.query(Card).filter(Card.board_id == board_id).all()



@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):

    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)
    return card


"""
@router.patch("/{card_id}", response_model=CardOut)
def update_card(card_id: int,
                data: CardUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(card, key, value)

    card.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(card)
    return card
"""
@router.put("/{card_id}", response_model=CardOut)
def update_card(
    card_id: int,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Edita una tarjeta existente.

    Reglas:
    - La tarjeta debe existir.
    - La tarjeta debe pertenecer a un board del usuario autenticado.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    # Seguridad: validamos permisos usando el board_id actual de la tarjeta
    verify_board_permission(card.board_id, current_user.id, db)

    # Aplicar cambios (solo si vienen en el body)
    if data.title is not None:
        card.title = data.title
    if data.description is not None:
        card.description = data.description
    if data.due_date is not None:
        card.due_date = data.due_date
    if data.list_id is not None:
        card.list_id = data.list_id

    card.updated_at = datetime.now(timezone.utc)

    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.patch("/{card_id}", response_model=CardOut)
def patch_card(
    card_id: int,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Edita parcialmente una tarjeta existente (PATCH).

    Reglas:
    - La tarjeta debe existir.
    - La tarjeta debe pertenecer a un board del usuario autenticado.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    # Seguridad: validamos permisos usando el board_id actual de la tarjeta
    verify_board_permission(card.board_id, current_user.id, db)

    # Aplicar cambios (solo si vienen en el body)
    if data.title is not None:
        card.title = data.title
    if data.description is not None:
        card.description = data.description
    if data.due_date is not None:
        card.due_date = data.due_date
    if data.list_id is not None:
        card.list_id = data.list_id

    card.updated_at = datetime.now(timezone.utc)

    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@router.get("/", response_model=list[CardOut])
def list_cards(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # seguridad: board existe y es del usuario
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")

    return db.query(Card).filter(Card.board_id == board_id).order_by(Card.id.desc()).all()

"""
@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(card)
    db.commit()
    return None
    """
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