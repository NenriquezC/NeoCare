"""
Rutas principales para gestión de tableros (Board) en la API.

Provee endpoints para consultar los tableros de cada usuario autenticado.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List as ListType

from ..auth.utils import get_current_user
from app.utils import get_db, get_board_or_404
from ..boards.models import User
from .models import Board, List, BoardMember   # ✅ FIX: importar BoardMember
from .schemas import BoardOut, ListOut

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("/", response_model=ListType[BoardOut])
def get_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene todos los tableros pertenecientes al usuario autenticado.

    Nota (importante):
        Si el usuario NO tiene tableros (usuarios antiguos creados antes de la creación automática),
        se crea automáticamente 1 tablero y sus 3 listas por defecto para evitar que el frontend
        quede bloqueado.
    """
    boards = (
        db.query(Board)
        .filter(Board.user_id == current_user.id)
        .order_by(Board.id)
        .all()
    )

    # ✅ CAMBIO: autocrear tablero + listas si el usuario no tiene ninguno
    if not boards:
        default_board = Board(name="Tablero principal", user_id=current_user.id)
        db.add(default_board)
        db.commit()
        db.refresh(default_board)

        # ✅ FIX CRÍTICO: registrar al creador como miembro del board
        membership = BoardMember(
            board_id=default_board.id,
            user_id=current_user.id,
        )
        db.add(membership)
        db.commit()

        default_lists = [
            List(name="Por hacer", board_id=default_board.id, position=0),
            List(name="En curso", board_id=default_board.id, position=1),
            List(name="Hecho", board_id=default_board.id, position=2),
        ]
        db.add_all(default_lists)
        db.commit()

        boards = [default_board]

    return boards


# ✅ CAMBIO: aceptar /lists y /lists/ para eliminar el 307 redirect
@router.get("/{board_id}/lists", response_model=ListType[ListOut])
@router.get("/{board_id}/lists/", response_model=ListType[ListOut])
def get_board_lists(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve las listas (columnas) de un tablero específico.

    Reglas de seguridad:
        - El tablero debe existir.
        - El tablero debe pertenecer al usuario autenticado.
    """

    board = get_board_or_404(db, board_id)
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")

    lists = (
        db.query(List)
        .filter(List.board_id == board_id)
        .order_by(List.position)
        .all()
    )

    # ✅ CAMBIO: autocrear listas si el tablero no tiene ninguna
    if not lists:
        default_lists = [
            List(name="Por hacer", board_id=board_id, position=0),
            List(name="En curso", board_id=board_id, position=1),
            List(name="Hecho", board_id=board_id, position=2),
        ]
        db.add_all(default_lists)
        db.commit()
        lists = default_lists

    return lists


from pydantic import BaseModel

class BoardUserOut(BaseModel):
    id: int
    name: str | None = None
    email: str
    role: str | None = None

    class Config:
        orm_mode = True


@router.get("/{board_id}/users", response_model=ListType[BoardUserOut], status_code=status.HTTP_200_OK)
def get_board_users(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve los usuarios miembros del board (incluyendo owner).
    Solo si el usuario autenticado tiene acceso al board.
    """
    board = get_board_or_404(db, board_id)
    # Permitir solo si es owner o miembro
    is_member = (
        db.query(BoardMember)
        .filter(BoardMember.board_id == board_id, BoardMember.user_id == current_user.id)
        .first()
    )
    if not (board.user_id == current_user.id or is_member):
        raise HTTPException(status_code=403, detail="No tienes permiso para este tablero")
    # Owner + miembros (sin duplicados)
    users = [board.owner]
    member_users = (
        db.query(User)
        .join(BoardMember, BoardMember.user_id == User.id)
        .filter(BoardMember.board_id == board_id)
        .all()
    )
    for u in member_users:
        if u.id != board.owner.id:
            users.append(u)
    return users
