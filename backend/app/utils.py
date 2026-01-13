"""
Utilidades y dependencias comunes para centralizar lógica repetida en NeoCare.
Incluye validaciones de permisos, búsquedas de entidades y utilidades generales.
"""
from fastapi import Depends, status
from app.error_shortcuts import not_found, forbidden
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.boards.models import Board, Card, BoardMember, List, Label, Subtask, TimeEntry
from app.auth.utils import get_current_user

# Dependencia para obtener la sesión de base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Búsquedas de entidades por ID ---

def get_board_or_404(db: Session, board_id: int) -> Board:
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        not_found("Tablero no encontrado")
    return board

def get_card_or_404(db: Session, card_id: int) -> Card:
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        not_found("Tarjeta no encontrada")
    return card

def get_list_or_404(db: Session, list_id: int) -> List:
    lista = db.query(List).filter(List.id == list_id).first()
    if not lista:
        not_found("Lista no encontrada")
    return lista

def get_label_or_404(db: Session, label_id: int) -> Label:
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        not_found("Etiqueta no encontrada")
    return label

def get_subtask_or_404(db: Session, subtask_id: int) -> Subtask:
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        not_found("Subtarea no encontrada")
    return subtask

def get_timeentry_or_404(db: Session, timeentry_id: int) -> TimeEntry:
    entry = db.query(TimeEntry).filter(TimeEntry.id == timeentry_id).first()
    if not entry:
        not_found("Registro no encontrado")
    return entry

# --- Validaciones de permisos ---

def require_board_member(db: Session, board_id: int, user_id: int):
    member = db.query(BoardMember).filter(BoardMember.board_id == board_id, BoardMember.user_id == user_id).first()
    if not member:
        forbidden("No tienes permiso para este tablero")
    return member

# --- Utilidad para obtener usuario actual (FastAPI Dependency) ---

def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        forbidden("Usuario inactivo")
    return current_user

# --- Validación de propiedad sobre recursos ---

def require_owner(resource_user_id: int, current_user_id: int):
    if resource_user_id != current_user_id:
        forbidden("No autorizado")

# --- Validación de rangos y formatos (ejemplo) ---

def validate_week_format(week: str):
    import re
    if not re.match(r"^\d{4}-W\d{2}$", week):
        from app.error_shortcuts import bad_request
        bad_request("Formato de semana inválido (usa YYYY-WXX)")
    return week

# Puedes agregar más utilidades según crezcan los módulos.
