from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta, timezone
from typing import List, Optional
import re

from .schemas import WorklogCreate, WorklogUpdate, WorklogOut
from ..auth.utils import get_current_user, get_db
from ..boards.models import Card, Board, User, TimeEntry, BoardMember

router = APIRouter(tags=["worklogs"])

def check_card_access(card_id: int, user_id: int, db: Session):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    board = db.query(Board).filter(Board.id == card.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    
    # El dueño del tablero tiene acceso
    if board.user_id == user_id:
        return card
    
    # Los miembros del tablero tienen acceso
    member = db.query(BoardMember).filter(
        BoardMember.board_id == board.id,
        BoardMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta tarjeta")
    
    return card

@router.post("/cards/{card_id}/worklogs", response_model=WorklogOut, status_code=status.HTTP_201_CREATED)
def create_worklog(
    card_id: int,
    data: WorklogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_card_access(card_id, current_user.id, db)
    
    new_worklog = TimeEntry(
        user_id=current_user.id,
        card_id=card_id,
        date=data.date,
        hours=data.hours,
        note=data.note,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(new_worklog)
    db.commit()
    db.refresh(new_worklog)
    return new_worklog

@router.get("/cards/{card_id}/worklogs", response_model=List[WorklogOut])
def get_card_worklogs(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_card_access(card_id, current_user.id, db)
    
    worklogs = db.query(TimeEntry).filter(TimeEntry.card_id == card_id).all()
    return worklogs

@router.patch("/worklogs/{id}", response_model=WorklogOut)
def update_worklog(
    id: int,
    data: WorklogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    worklog = db.query(TimeEntry).filter(TimeEntry.id == id).first()
    if not worklog:
        raise HTTPException(status_code=404, detail="Registro de tiempo no encontrado")
    
    if worklog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el autor puede editar su registro")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(worklog, key, value)
    
    worklog.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(worklog)
    return worklog

@router.delete("/worklogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_worklog(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    worklog = db.query(TimeEntry).filter(TimeEntry.id == id).first()
    if not worklog:
        raise HTTPException(status_code=404, detail="Registro de tiempo no encontrado")
    
    if worklog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el autor puede eliminar su registro")
    
    db.delete(worklog)
    db.commit()
    return None

@router.get("/users/me/worklogs", response_model=List[WorklogOut])
def get_my_worklogs(
    week: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(TimeEntry).filter(TimeEntry.user_id == current_user.id)
    
    if week:
        try:
            year, wk = map(int, week.split('-'))
            # ISO week starts on Monday (1)
            start_date = date.fromisocalendar(year, wk, 1)
            end_date = date.fromisocalendar(year, wk, 7)
            query = query.filter(TimeEntry.date >= start_date, TimeEntry.date <= end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de semana inválido. Use YYYY-WW")
            
    return query.all()
