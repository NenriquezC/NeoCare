"""
Rutas principales para gestión de tableros (Board) en la API.

Provee endpoints para consultar los tableros de cada usuario autenticado.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List as ListType

from ..auth.utils import get_current_user, get_db
from ..boards.models import User
from .models import Board, List
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
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")

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


# CAMBIOS REALIZADOS Y POR QUÉ:
# 1) get_boards(): si el usuario no tiene boards, se crea automáticamente:
#    - 1 board "Tablero principal"
#    - 3 listas con position 0/1/2
#    Esto elimina el error del frontend: "No hay tablero disponible para tu usuario".
# 2) Se mantiene tu fix para aceptar /lists y /lists/ y evitar el 307 redirect.