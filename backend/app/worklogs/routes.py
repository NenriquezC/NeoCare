"""
Rutas API para Worklogs (registro de horas) — Semana 4.

Implementa:
- Crear horas por tarjeta
- Listar horas por tarjeta
- Editar horas (solo autor)
- Eliminar horas (solo autor)
- Ver horas del usuario por semana
"""

from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..auth.utils import get_current_user
from ..auth.utils import get_db, get_current_user
from ..boards.models import TimeEntry, Card, BoardMember, Board
from .schemas import (
    WorklogCreate,
    WorklogUpdate,
    WorklogOut,
    MyHoursWeekSummary,
    MyHoursDayTotal,
)

router = APIRouter(prefix="/worklogs", tags=["worklogs"])


# ---------------------------------------------------------------------
# CREAR WORKLOG
# ---------------------------------------------------------------------
@router.post("/", response_model=WorklogOut, status_code=status.HTTP_201_CREATED)
def create_worklog(
    data: WorklogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Crear un registro de horas para una tarjeta.
    """

    card = db.query(Card).filter(Card.id == data.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    # Verificar que el usuario pertenece al board de la tarjeta o es el dueño
    membership = (
        db.query(BoardMember)
        .filter(
            BoardMember.board_id == card.board_id,
            BoardMember.user_id == current_user.id,
        )
        .first()
    )

    # Si no hay membresía, verificamos si es el dueño del tablero
    is_owner = card.board.user_id == current_user.id

    if not membership and not is_owner:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a esta tarjeta",
        )

    worklog = TimeEntry(
        user_id=current_user.id,
        card_id=data.card_id,
        date=data.date,
        hours=data.hours,
        note=data.note,
    )

    db.add(worklog)
    db.commit()
    db.refresh(worklog)

    return worklog


# ---------------------------------------------------------------------
# LISTAR WORKLOGS POR TARJETA
# ---------------------------------------------------------------------
@router.get("/card/{card_id}", response_model=List[WorklogOut])
def list_worklogs_by_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Listar horas asociadas a una tarjeta.
    """

    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    # Verificar que el usuario es owner o miembro del board
    board = db.query(Board).filter(Board.id == card.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    
    is_owner = board.user_id == current_user.id
    is_member = (
        db.query(BoardMember)
        .filter(
            BoardMember.board_id == card.board_id,
            BoardMember.user_id == current_user.id,
        )
        .first()
    ) is not None

    if not is_owner and not is_member:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return (
        db.query(TimeEntry)
        .filter(TimeEntry.card_id == card_id)
        .order_by(TimeEntry.date.desc())
        .all()
    )


# ---------------------------------------------------------------------
# EDITAR WORKLOG
# ---------------------------------------------------------------------
@router.put("/{worklog_id}", response_model=WorklogOut)
def update_worklog(
    worklog_id: int,
    data: WorklogUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Editar un registro de horas (solo el autor).
    """

    worklog = db.query(TimeEntry).filter(TimeEntry.id == worklog_id).first()
    if not worklog:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if worklog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    if data.date is not None:
        worklog.date = data.date
    if data.hours is not None:
        worklog.hours = data.hours
    if data.note is not None:
        worklog.note = data.note

    db.commit()
    db.refresh(worklog)

    return worklog


# ---------------------------------------------------------------------
# ELIMINAR WORKLOG
# ---------------------------------------------------------------------
@router.delete("/{worklog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_worklog(
    worklog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Eliminar un registro de horas (solo el autor).
    """

    worklog = db.query(TimeEntry).filter(TimeEntry.id == worklog_id).first()
    if not worklog:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if worklog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    db.delete(worklog)
    db.commit()


# ---------------------------------------------------------------------
# MIS HORAS — RESUMEN SEMANAL
# ---------------------------------------------------------------------
@router.get("/me/week", response_model=MyHoursWeekSummary)
def my_hours_week(
    week: str = Query(None, description="Semana en formato YYYY-WW (opcional, por defecto semana actual)"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Ver horas del usuario por semana (YYYY-WW).
    Si no se especifica semana, usa la semana actual.
    """
    
    # Si no se proporciona semana, calcular la semana actual
    if not week:
        today = date.today()
        iso_cal = today.isocalendar()
        week = f"{iso_cal[0]}-W{iso_cal[1]:02d}"

    try:
        year, week_num = map(int, week.split("-W"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de semana inválido (usa YYYY-WXX)")

    first_day = date.fromisocalendar(year, week_num, 1)
    last_day = first_day + timedelta(days=6)

    entries = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.user_id == current_user.id,
            TimeEntry.date.between(first_day, last_day),
        )
        .all()
    )

    totals = (
        db.query(
            TimeEntry.date,
            func.sum(TimeEntry.hours).label("total_hours"),
        )
        .filter(
            TimeEntry.user_id == current_user.id,
            TimeEntry.date.between(first_day, last_day),
        )
        .group_by(TimeEntry.date)
        .all()
    )

    return MyHoursWeekSummary(
        week=week,
        total_hours=sum(t.total_hours for t in totals),
        by_day=[
            MyHoursDayTotal(date=t.date, total_hours=t.total_hours)
            for t in totals
        ],
        entries=entries,
    )