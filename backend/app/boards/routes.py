"""
Rutas principales para gestión de tableros (Board) en la API.

Provee endpoints para consultar los tableros de cada usuario autenticado.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.utils import get_current_user, get_db
from .models import Board
from ..boards.models import User

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("/")
def get_boards(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    """
    Obtiene todos los tableros pertenecientes al usuario autenticado.

    Parámetros:
        db (Session): Sesión actual de la base de datos inyectada por FastAPI.
        current_user (User): Usuario autenticado inyectado por FastAPI.

    Retorna:
        List[Board]: Lista de objetos Board que pertenecen al usuario actual.
    """
    return db.query(Board).filter(Board.user_id == current_user.id).all()