from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .schemas import (
    CardCreate, CardUpdate, CardOut, CardMove,
    LabelCreate, LabelOut, SubtaskCreate, SubtaskUpdate, SubtaskOut
)
from ..auth.utils import get_current_user, get_db
from ..boards.models import Card, Board, List, User, Label, Subtask
from sqlalchemy import or_

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
        #raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")
        raise HTTPException(status_code=403)

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
    list_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    📋 SEMANA 6 - Obtiene tarjetas con búsqueda y filtrado avanzado
    
    Query Parameters:
    - board_id (requerido): ID del tablero
    - search (opcional): Busca en título y descripción (case-insensitive)
    - responsible_id (opcional): Filtra por usuario responsable
    - list_id (opcional): Filtra por lista específica
    
    Ejemplo Frontend:
    ```javascript
    // Buscar "urgente" en tablero 1
    GET /cards?board_id=1&search=urgente
    
    // Filtrar por responsable
    GET /cards?board_id=1&responsible_id=5
    
    // Combinar filtros
    GET /cards?board_id=1&search=API&responsible_id=5&list_id=2
    ```
    
    Response: Lista de CardOut con labels y subtasks incluidos
    """
    verify_board_permission(board_id, current_user.id, db)

    # Construcción de query base
    query = db.query(Card).filter(Card.board_id == board_id)

    # 🔍 BÚSQUEDA: Filtra por título o descripción
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Card.title.ilike(search_pattern)) | 
            (Card.description.ilike(search_pattern))
        )
    
    # 👤 FILTRO POR RESPONSABLE
    if responsible_id:
        query = query.filter(Card.responsible_id == responsible_id)
    
    # 📂 FILTRO POR LISTA
    if list_id:
        query = query.filter(Card.list_id == list_id)

    # Ordenar por lista y posición
    return query.order_by(Card.list_id, Card.position).all()

    if responsible_id is not None:
        query_db = query_db.filter(Card.responsible_id == responsible_id)

    return query_db.order_by(Card.list_id, Card.position).all()

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

    # Eliminar la tarjeta - SQLAlchemy manejará las relaciones con cascade
    db.delete(card)
    db.commit()
    return None


# =====================================================================================
# 🏷️ SEMANA 6 - LABELS (ETIQUETAS)
# =====================================================================================
"""
Las etiquetas permiten categorizar y priorizar tarjetas con colores y nombres.

CASOS DE USO:
- Prioridad: "Urgente" (rojo), "Media" (amarillo), "Baja" (verde)
- Categorías: "Bug" (rojo), "Feature" (azul), "QA" (púrpura)
- Dependencias: "Bloqueado" (gris), "En revisión" (naranja)

FLUJO FRONTEND:
1. Usuario abre modal de edición de tarjeta
2. Sección de labels muestra las actuales como chips con colores
3. Botón "Añadir etiqueta" abre selector de colores predefinidos
4. POST /cards/{card_id}/labels con {name, color}
5. La etiqueta aparece inmediatamente en la tarjeta
6. Click en X de la etiqueta → DELETE /cards/labels/{label_id}
"""


@router.post("/{card_id}/labels", response_model=LabelOut)
def add_label(
    card_id: int,
    data: LabelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    🏷️ Añade una etiqueta a una tarjeta
    
    Body JSON:
    {
        "name": "Urgente",
        "color": "#ef4444"  // Hex color o nombre
    }
    
    Colores sugeridos para Frontend:
    - Rojo: #ef4444 (urgente, bugs)
    - Amarillo: #f59e0b (media prioridad)
    - Verde: #10b981 (baja prioridad, completado)
    - Azul: #3b82f6 (features, info)
    - Púrpura: #8b5cf6 (QA, testing)
    - Gris: #6b7280 (bloqueado, pausado)
    
    Ejemplo Frontend (React):
    ```javascript
    const addLabel = async (cardId, labelData) => {
        const response = await fetch(`/cards/${cardId}/labels`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(labelData)
        });
        return response.json();
    };
    
    // Uso
    await addLabel(123, { name: "Urgente", color: "#ef4444" });
    ```
    
    Response: LabelOut con id, card_id, name, color
    """
    # Verificar que la tarjeta existe y el usuario tiene permiso
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)

    # Crear la etiqueta
    new_label = Label(
        card_id=card_id, 
        name=data.name, 
        color=data.color or "#6b7280"  # Color por defecto: gris
    )
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label


@router.get("/{card_id}/labels", response_model=list[LabelOut])
def get_card_labels(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    🏷️ Obtiene todas las etiquetas de una tarjeta
    
    Ejemplo Frontend:
    ```javascript
    const labels = await fetch(`/cards/${cardId}/labels`, {
        headers: { 'Authorization': `Bearer ${token}` }
    }).then(r => r.json());
    
    // Renderizar
    labels.map(label => (
        <span style={{ backgroundColor: label.color }} 
              className="px-2 py-1 rounded text-xs">
            {label.name}
        </span>
    ))
    ```
    
    Response: Array de LabelOut
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)
    
    return db.query(Label).filter(Label.card_id == card_id).all()


@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_label(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    🏷️ Elimina una etiqueta por su ID
    
    Ejemplo Frontend:
    ```javascript
    const deleteLabel = async (labelId) => {
        await fetch(`/cards/labels/${labelId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    };
    ```
    
    Response: 204 No Content (éxito)
    """
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    
    # Verificar permisos a través de la tarjeta
    card = db.query(Card).filter(Card.id == label.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(label)
    db.commit()
    return None


# =====================================================================================
# ✅ SEMANA 6 - SUBTASKS (CHECKLIST)
# =====================================================================================
"""
Las subtasks permiten dividir una tarjeta en tareas más pequeñas con checklist.

CASOS DE USO:
- Desglosar una card compleja en pasos
- Mostrar progreso visual (3/7 completadas)
- Seguimiento de hitos dentro de una feature

FLUJO FRONTEND:
1. Usuario abre modal de tarjeta
2. Sección "Checklist" muestra subtasks con checkboxes
3. Barra de progreso: "✓ 3/7 completadas (43%)"
4. Input para añadir nueva subtask → POST /cards/{card_id}/subtasks
5. Click en checkbox → PATCH /subtasks/{id} con {completed: true}
6. Botón eliminar → DELETE /subtasks/{id}
"""


@router.post("/{card_id}/subtasks", response_model=SubtaskOut)
def add_subtask(
    card_id: int,
    data: SubtaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ✅ Añade una subtarea (item de checklist) a una tarjeta
    
    Body JSON:
    {
        "title": "Escribir documentación de API",
        "completed": false  // Opcional, default false
    }
    
    Ejemplo Frontend (React):
    ```javascript
    const addSubtask = async (cardId, title) => {
        const response = await fetch(`/cards/${cardId}/subtasks`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, completed: false })
        });
        return response.json();
    };
    
    // Uso
    await addSubtask(123, "Implementar endpoint de búsqueda");
    ```
    
    Response: SubtaskOut con id, card_id, title, completed, position
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)

    # Calcular posición automática (al final de la lista)
    max_pos = db.query(Subtask).filter(Subtask.card_id == card_id).count()

    new_subtask = Subtask(
        card_id=card_id, 
        title=data.title,
        completed=data.completed if hasattr(data, 'completed') else False,
        position=max_pos
    )
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    return new_subtask


@router.get("/{card_id}/subtasks", response_model=list[SubtaskOut])
def get_card_subtasks(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ✅ Obtiene todas las subtareas de una tarjeta
    
    Ejemplo Frontend con barra de progreso:
    ```javascript
    const subtasks = await fetch(`/cards/${cardId}/subtasks`, {
        headers: { 'Authorization': `Bearer ${token}` }
    }).then(r => r.json());
    
    const completed = subtasks.filter(s => s.completed).length;
    const total = subtasks.length;
    const percentage = Math.round((completed / total) * 100);
    
    // Renderizar
    <div>
        <h3>Checklist: {completed}/{total} completadas</h3>
        <div className="progress-bar">
            <div style={{ width: `${percentage}%` }} />
        </div>
        {subtasks.map(st => (
            <label key={st.id}>
                <input type="checkbox" 
                       checked={st.completed}
                       onChange={() => toggleSubtask(st.id)} />
                <span className={st.completed ? 'line-through' : ''}>
                    {st.title}
                </span>
            </label>
        ))}
    </div>
    ```
    
    Response: Array de SubtaskOut ordenado por position
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    verify_board_permission(card.board_id, current_user.id, db)
    
    return (
        db.query(Subtask)
        .filter(Subtask.card_id == card_id)
        .order_by(Subtask.position)
        .all()
    )


@router.patch("/subtasks/{subtask_id}", response_model=SubtaskOut)
def update_subtask(
    subtask_id: int,
    data: SubtaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ✅ Actualiza una subtarea (título, completado, posición)
    
    Body JSON (todos los campos opcionales):
    {
        "title": "Nuevo título",          // Opcional
        "completed": true,                 // Opcional
        "position": 2                      // Opcional (para reordenar)
    }
    
    Ejemplo Frontend - Marcar como completada:
    ```javascript
    const toggleSubtask = async (subtaskId, currentCompleted) => {
        await fetch(`/cards/subtasks/${subtaskId}`, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ completed: !currentCompleted })
        });
    };
    ```
    
    Ejemplo Frontend - Editar título:
    ```javascript
    const updateSubtaskTitle = async (subtaskId, newTitle) => {
        await fetch(`/cards/subtasks/${subtaskId}`, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title: newTitle })
        });
    };
    ```
    
    Response: SubtaskOut actualizado
    """
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtarea no encontrada")
    
    # Verificar permisos
    card = db.query(Card).filter(Card.id == subtask.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    # Actualizar solo los campos que vienen en el body
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subtask, field, value)

    db.commit()
    db.refresh(subtask)
    return subtask


@router.delete("/subtasks/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask(
    subtask_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ✅ Elimina una subtarea
    
    Ejemplo Frontend:
    ```javascript
    const deleteSubtask = async (subtaskId) => {
        await fetch(`/cards/subtasks/${subtaskId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    };
    ```
    
    Response: 204 No Content (éxito)
    """
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtarea no encontrada")
    
    # Verificar permisos
    card = db.query(Card).filter(Card.id == subtask.card_id).first()
    verify_board_permission(card.board_id, current_user.id, db)

    db.delete(subtask)
    db.commit()
    return None
