# tests/boards/test_routes.py
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

from app.boards.models import Board
from app.main import app
from app.auth.utils import get_db, get_current_user

client = TestClient(app)

def test_get_boards_exitoso():
    # usuario falso
    fake_user = MagicMock()
    fake_user.id = 123

    # boards REALES
    fake_boards = [
        Board(id=1, name="Board 1", user_id=123),
        Board(id=2, name="Board 2", user_id=123),
    ]

    # sesión falsa
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.all.return_value = fake_boards

    # overrides
    def override_get_user():
        return fake_user

    def override_get_db():
        yield mock_session

    app.dependency_overrides[get_current_user] = override_get_user
    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/boards/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Board 1"
    assert data[1]["name"] == "Board 2"

    app.dependency_overrides.clear()