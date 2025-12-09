# tests/test_models.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember
from datetime import date

# -------------------------
# Configurar DB en memoria
# -------------------------
engine = create_engine("sqlite:///:memory:", echo=False)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# -------------------------
# Tests User
# -------------------------
def test_create_user(setup_db):
    db = setup_db
    user = User(email="test@example.com", password_hash="hashed_pw", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"

# -------------------------
# Tests Board
# -------------------------
def test_create_board(setup_db):
    db = setup_db
    user = User(email="owner@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Proyecto 1", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    assert board.id is not None
    assert board.owner == user
    assert board.name == "Proyecto 1"

# -------------------------
# Tests List
# -------------------------
def test_create_list(setup_db):
    db = setup_db
    user = User(email="listowner@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board List", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="To Do", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    assert list_.id is not None
    assert list_.board == board
    assert list_.position == 1

# -------------------------
# Tests Card
# -------------------------
def test_create_card(setup_db):
    db = setup_db
    user = User(email="carduser@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Card", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="Doing", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    card = Card(
        title="Tarea 1",
        board=board,
        list=list_,
        board_id=board.id,
        list_id=list_.id,
        created_by=user,
        created_by_id=user.id,
        responsible=user,
        responsible_id=user.id,
        position=1,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    assert card.id is not None
    assert card.board == board
    assert card.list == list_
    assert card.created_by == user
    assert card.responsible == user

# -------------------------
# Tests TimeEntry
# -------------------------
def test_create_time_entry(setup_db):
    db = setup_db
    user = User(email="timeuser@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Time", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="List Time", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    card = Card(
        title="Card Time",
        board=board,
        list=list_,
        board_id=board.id,
        list_id=list_.id,
        created_by=user,
        created_by_id=user.id,
        responsible=user,
        responsible_id=user.id,
        position=1,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    entry = TimeEntry(user=user, user_id=user.id, card=card, card_id=card.id, date=date.today(), hours=2.5)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    assert entry.id is not None
    assert entry.user == user
    assert entry.card == card
    assert entry.hours == 2.5

# -------------------------
# Tests BoardMember
# -------------------------
def test_create_board_member(setup_db):
    db = setup_db
    user = User(email="member@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Member", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    member = BoardMember(board=board, board_id=board.id, user=user, user_id=user.id, role="admin")
    db.add(member)
    db.commit()
    db.refresh(member)

    assert member.id is not None
    assert member.board == board
    assert member.user == user
    assert member.role == "admin"
