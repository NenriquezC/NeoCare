from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.utils import get_current_user, get_db
from .models import Board
from ..boards.models import User

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("/")
def get_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Board).filter(Board.user_id == current_user.id).all()