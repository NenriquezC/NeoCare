from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List as ListType
from datetime import datetime, time

from ..auth.utils import get_db, get_current_user
from ..boards.models import Board, List, Card, TimeEntry, User, BoardMember
from .schemas import ReportSummary, UserHoursReport, CardHoursReport
from .utils import get_week_range

router = APIRouter(prefix="/report", tags=["reports"])

def verify_board_access(board_id: int, user_id: int, db: Session):
    # Verificar si es dueño o miembro
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    
    if board.user_id == user_id:
        return board
        
    membership = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="No tienes acceso a este tablero")
    
    return board

@router.get("/{board_id}/summary", response_model=ReportSummary)
def get_report_summary(
    board_id: int,
    week: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_board_access(board_id, current_user.id, db)
    
    try:
        start_date, end_date = get_week_range(week)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Convertir fechas a datetime para comparar con created_at/updated_at
    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)

    # Buscar la lista "Hecho" para este tablero
    hecho_list = db.query(List).filter(
        List.board_id == board_id,
        List.name.ilike("Hecho")
    ).first()
    hecho_id = hecho_list.id if hecho_list else -1

    # 1. Completadas: list_id = 'Hecho' y updated_at en la semana
    completed = db.query(Card).filter(
        Card.board_id == board_id,
        Card.list_id == hecho_id,
        Card.updated_at >= start_dt,
        Card.updated_at <= end_dt
    ).count()

    # 2. Vencidas: due_date en la semana y list_id != 'Hecho'
    overdue = db.query(Card).filter(
        Card.board_id == board_id,
        Card.list_id != hecho_id,
        Card.due_date >= start_date,
        Card.due_date <= end_date
    ).count()

    # 3. Nuevas: created_at en la semana
    new_cards = db.query(Card).filter(
        Card.board_id == board_id,
        Card.created_at >= start_dt,
        Card.created_at <= end_dt
    ).count()

    return {
        "completed": completed,
        "overdue": overdue,
        "new": new_cards
    }

@router.get("/{board_id}/hours-by-user", response_model=ListType[UserHoursReport])
def get_hours_by_user(
    board_id: int,
    week: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_board_access(board_id, current_user.id, db)
    
    try:
        start_date, end_date = get_week_range(week)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Consulta: Suma de horas y conteo de tareas distintas por usuario en ese tablero y semana
    results = db.query(
        User.id,
        User.name,
        func.sum(TimeEntry.hours).label("total_hours"),
        func.count(func.distinct(TimeEntry.card_id)).label("tasks_count")
    ).join(TimeEntry, User.id == TimeEntry.user_id)\
     .join(Card, TimeEntry.card_id == Card.id)\
     .filter(
         Card.board_id == board_id,
         TimeEntry.date >= start_date,
         TimeEntry.date <= end_date
     ).group_by(User.id, User.name).all()

    return [
        {
            "user_id": r.id,
            "user_name": r.name,
            "total_hours": r.total_hours or 0,
            "tasks_count": r.tasks_count
        } for r in results
    ]

@router.get("/{board_id}/hours-by-card", response_model=ListType[CardHoursReport])
def get_hours_by_card(
    board_id: int,
    week: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_board_access(board_id, current_user.id, db)
    
    try:
        start_date, end_date = get_week_range(week)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Consulta: Suma de horas por tarjeta en ese tablero y semana
    results = db.query(
        Card.id,
        Card.title,
        User.name.label("responsible_name"),
        List.name.label("status_name"),
        func.sum(TimeEntry.hours).label("total_hours")
    ).join(TimeEntry, Card.id == TimeEntry.card_id)\
     .outerjoin(User, Card.responsible_id == User.id)\
     .join(List, Card.list_id == List.id)\
     .filter(
         Card.board_id == board_id,
         TimeEntry.date >= start_date,
         TimeEntry.date <= end_date
     ).group_by(Card.id, Card.title, User.name, List.name).all()

    return [
        {
            "card_id": r.id,
            "title": r.title,
            "responsible": r.responsible_name,
            "status": r.status_name,
            "total_hours": r.total_hours or 0
        } for r in results
    ]
