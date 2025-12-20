from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.boards.schemas import BoardBase, BoardOut
from app.auth.routes import get_current_user

boards_router = APIRouter()

@boards_router.post("/", response_model=BoardOut)
def create_board(board: BoardBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_board = models.Board(title=board.title, owner_id=user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@boards_router.get("/", response_model=list[BoardOut])
def get_user_boards(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Board).filter(models.Board.owner_id == user.id).all()

@boards_router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    board = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.owner_id == user.id
    ).first()

    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")

    db.delete(board)
    db.commit()
    return {"message": "Board eliminado"}
