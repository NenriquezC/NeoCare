# tests/boards/test_routes.py
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.boards.models import Board
from app.boards.models import User as UserModel  # Evitar conflictos de nombres

client = TestClient(app)

# Datos de ejemplo
fake_user = MagicMock()
fake_user.id = 1

fake_boards = [
    MagicMock(spec=Board, id=1, name="Board 1", user_id=fake_user.id),
    MagicMock(spec=Board, id=2, name="Board 2", user_id=fake_user.id),
]

# ----------------------------
# Test GET /boards/
# ----------------------------
@patch("backend.boards.routers.get_db")
@patch("backend.boards.routers.get_current_user")
def test_get_boards_exitoso(mock_get_user, mock_get_db):
    # Mock de usuario
    mock_get_user.return_value = fake_user

    # Mock de DB
    mock_session = MagicMock()
    query_mock = mock_session.query.return_value
    filter_mock = query_mock.filter.return_value
    filter_mock.all.return_value = fake_boards
    mock_get_db.return_value = mock_session

    response = client.get("/boards/")
    assert response.status_code == 200
    data = response.json()

    # Comprobamos que la respuesta contiene las boards simuladas
    assert len(data) == 2
    assert data[0]["name"] == "Board 1"
    assert data[1]["name"] == "Board 2"

    # Verificamos llamadas a la DB
    mock_session.query.assert_called_once_with(Board)
    query_mock.filter.assert_called_once()
    filter_mock.all.assert_called_once()

# ----------------------------
# Test GET /boards/ sin boards
# ----------------------------
@patch("backend.boards.routers.get_db")
@patch("backend.boards.routers.get_current_user")
def test_get_boards_vacio(mock_get_user, mock_get_db):
    mock_get_user.return_value = fake_user
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.all.return_value = []
    mock_get_db.return_value = mock_session

    response = client.get("/boards/")
    assert response.status_code == 200
    data = response.json()
    assert data == []  # Lista vacía
