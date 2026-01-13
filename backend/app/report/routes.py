"""
Rutas del módulo Report — Semana 5.

Este módulo expone los endpoints HTTP necesarios para generar informes
semanales a partir de los datos existentes del sistema Kanban.

Responsabilidades:
- Definir endpoints REST del informe semanal.
- Orquestar autenticación, permisos y servicios.
- Mantener la lógica de negocio pesada fuera de las rutas.

Endpoints implementados:
- GET /report/{board_id}/summary
- GET /report/{board_id}/hours-by-user
- GET /report/{board_id}/hours-by-card
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_

from ..auth.utils import get_current_user
from app.utils import get_db, get_board_or_404
from ..boards.models import Card, List, TimeEntry, User
from .services import get_week_date_range, verify_board_access
from .schemas import WeeklySummaryResponse, SummaryBlock, CardSummaryItem

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get(
    "/{board_id}/summary",
    response_model=WeeklySummaryResponse
)
def get_weekly_summary(
    board_id: int,
    week: str = Query(..., description="Semana en formato ISO YYYY-WW"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Obtiene el resumen semanal de un tablero Kanban.

    El resumen incluye:
    - Tareas completadas durante la semana.
    - Tareas nuevas creadas durante la semana.
    - Tareas vencidas en la semana.

    Seguridad:
    - Requiere JWT válido.
    - El usuario debe ser owner o miembro del tablero.

    Args:
        board_id (int): ID del tablero a consultar.
        week (str): Semana ISO en formato 'YYYY-WW'.
        db (Session): Sesión de base de datos.
        current_user (User): Usuario autenticado.

    Returns:
        WeeklySummaryResponse: Resumen semanal estructurado y tipado.
    """
    # 1️⃣ Verificar acceso al tablero
    verify_board_access(db, board_id, current_user.id)

    # 2️⃣ Calcular rango de fechas de la semana
    start_date, end_date = get_week_date_range(week)

    # 3️⃣ Obtener la lista "Hecho" del tablero
    done_list = (
        db.query(List)
        .filter(
            List.board_id == board_id,
            List.name == "Hecho"
        )
        .first()
    )
    done_list_id = done_list.id if done_list else None

    # 4️⃣ Consultar tarjetas COMPLETADAS (optimizado con query SQL filtrado)
    # Criterio: completed_at dentro de la semana O (list_id=Hecho Y updated_at en semana como fallback)
    from sqlalchemy.orm import joinedload
    from datetime import datetime, timezone

    start_datetime = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_datetime = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)

    completed_query = db.query(Card).filter(Card.board_id == board_id)
    if done_list_id:
        # Tarjetas con completed_at en la semana O en lista Hecho con updated_at en semana
        completed_query = completed_query.filter(
            or_(
                and_(
                    Card.completed_at.isnot(None),
                    Card.completed_at >= start_datetime,
                    Card.completed_at <= end_datetime
                ),
                and_(
                    Card.list_id == done_list_id,
                    Card.completed_at.is_(None),
                    Card.updated_at >= start_datetime,
                    Card.updated_at <= end_datetime
                )
            )
        )
    else:
        # Sin lista "Hecho", solo usar completed_at
        completed_query = completed_query.filter(
            Card.completed_at.isnot(None),
            Card.completed_at >= start_datetime,
            Card.completed_at <= end_datetime
        )

    completed_cards = completed_query.options(joinedload(Card.responsible)).limit(10).all()
    completed_items = [
        CardSummaryItem(id=card.id, title=card.title, responsible_id=card.responsible_id)
        for card in completed_cards
    ]

    # 5️⃣ Consultar tarjetas NUEVAS (creadas en la semana)
    new_cards = (
        db.query(Card)
        .filter(
            Card.board_id == board_id,
            Card.created_at >= start_datetime,
            Card.created_at <= end_datetime
        )
        .options(joinedload(Card.responsible))
        .limit(10)
        .all()
    )
    new_items = [
        CardSummaryItem(id=card.id, title=card.title, responsible_id=card.responsible_id)
        for card in new_cards
    ]

    # 6️⃣ Consultar tarjetas VENCIDAS (due_date en la semana y NO completadas)
    overdue_query = (
        db.query(Card)
        .filter(
            Card.board_id == board_id,
            Card.due_date.isnot(None),
            Card.due_date >= start_date,
            Card.due_date <= end_date
        )
    )

    if done_list_id:
        # Excluir tarjetas completadas (tienen completed_at O están en lista Hecho)
        overdue_query = overdue_query.filter(
            Card.completed_at.is_(None),
            Card.list_id != done_list_id
        )
    else:
        overdue_query = overdue_query.filter(Card.completed_at.is_(None))

    overdue_cards = overdue_query.options(joinedload(Card.responsible)).limit(10).all()
    overdue_items = [
        CardSummaryItem(id=card.id, title=card.title, responsible_id=card.responsible_id)
        for card in overdue_cards
    ]

    # 7️⃣ Construir respuesta tipada con counts reales
    return WeeklySummaryResponse(
        week=week,
        completed=SummaryBlock(
            count=len(completed_items),
            items=completed_items[:5]  # Solo top 5 para UI
        ),
        new=SummaryBlock(
            count=len(new_items),
            items=new_items[:5]
        ),
        overdue=SummaryBlock(
            count=len(overdue_items),
            items=overdue_items[:5]
        ),
    )


@router.get(
    "/{board_id}/hours-by-user"
)
def get_hours_by_user(
    board_id: int,
    week: str = Query(..., description="Semana en formato ISO YYYY-WW"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Obtiene el total de horas trabajadas por usuario en una semana específica.

    Agrupa los registros de tiempo (TimeEntry) por usuario, sumando las horas
    trabajadas y contando el número de tarjetas distintas en las que participó.

    Seguridad:
    - Requiere JWT válido.
    - El usuario debe ser owner o miembro del tablero.

    Args:
        board_id (int): ID del tablero.
        week (str): Semana ISO en formato 'YYYY-WW'.
        db (Session): Sesión de base de datos.
        current_user (User): Usuario autenticado.

    Returns:
        list[dict]: Lista de usuarios con horas totales y número de tarjetas.
    """
    # 1️⃣ Verificar acceso al tablero
    verify_board_access(db, board_id, current_user.id)

    # 2️⃣ Calcular rango semanal
    start_date, end_date = get_week_date_range(week)

    # 3️⃣ Consulta agregada por usuario
    rows = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            func.coalesce(func.sum(TimeEntry.hours), 0).label("total_hours"),
            func.count(func.distinct(TimeEntry.card_id)).label("tasks_count"),
        )
        .join(TimeEntry, TimeEntry.user_id == User.id)
        .join(Card, Card.id == TimeEntry.card_id)
        .filter(
            Card.board_id == board_id,
            TimeEntry.date >= start_date,
            TimeEntry.date <= end_date,
        )
        .group_by(User.id, User.name)
        .all()
    )

    return [
        {
            "user_id": row.user_id,
            "user_name": row.user_name,
            "total_hours": float(row.total_hours),
            "tasks_count": row.tasks_count,
        }
        for row in rows
    ]


@router.get(
    "/{board_id}/hours-by-card"
)
def get_hours_by_card(
    board_id: int,
    week: str = Query(..., description="Semana en formato ISO YYYY-WW"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Obtiene el total de horas trabajadas por tarjeta en una semana específica.

    Agrupa los registros de tiempo por tarjeta, permitiendo analizar
    en qué tareas se concentró el esfuerzo semanal.

    Seguridad:
    - Requiere JWT válido.
    - El usuario debe ser owner o miembro del tablero.

    Args:
        board_id (int): ID del tablero.
        week (str): Semana ISO en formato 'YYYY-WW'.
        db (Session): Sesión de base de datos.
        current_user (User): Usuario autenticado.

    Returns:
        list[dict]: Lista de tarjetas con horas totales trabajadas,
                    ordenadas de mayor a menor.
    """
    # 1️⃣ Verificar acceso al tablero
    verify_board_access(db, board_id, current_user.id)

    # 2️⃣ Calcular rango semanal
    start_date, end_date = get_week_date_range(week)

    # 3️⃣ Consulta agregada por tarjeta
    rows = (
        db.query(
            Card.id.label("card_id"),
            Card.title.label("title"),
            User.name.label("responsible"),
            List.name.label("status"),
            func.coalesce(func.sum(TimeEntry.hours), 0).label("total_hours"),
        )
        .join(TimeEntry, TimeEntry.card_id == Card.id)
        .join(List, List.id == Card.list_id)
        .outerjoin(User, User.id == Card.responsible_id)
        .filter(
            Card.board_id == board_id,
            TimeEntry.date >= start_date,
            TimeEntry.date <= end_date,
        )
        .group_by(Card.id, Card.title, User.name, List.name)
        .order_by(func.sum(TimeEntry.hours).desc())
        .all()
    )

    return [
        {
            "card_id": row.card_id,
            "title": row.title,
            "responsible": row.responsible,
            "status": row.status,
            "total_hours": float(row.total_hours),
        }
        for row in rows
    ]