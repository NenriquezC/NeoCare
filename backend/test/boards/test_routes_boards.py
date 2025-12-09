"""
tests/boards/test_routes.py
---------------------------

Pruebas para las rutas del recurso "boards" usando TestClient de FastAPI.

Este módulo añade únicamente comentarios y docstrings explicativos sobre la
intención de las pruebas, los mocks y las comprobaciones realizadas. No se
modifica la lógica original de las pruebas ni su comportamiento.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.boards.models import Board
from app.boards.models import User as UserModel  # Evitar conflictos de nombres

# Cliente de pruebas para la aplicación FastAPI
client = TestClient(app)

# Datos de ejemplo y mocks reusables
# fake_user simula al usuario autenticado que retornará el mock de get_current
fake_user = MagicMock()
fake_user.id = 1

# fake_boards simula una lista de objetos Board retornados por la consulta a la DB
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
    """
    Verifica la respuesta exitosa al obtener la lista de boards del usuario.

    Flujo:
    - Se parchea `get_current_user` para devolver un usuario simulado (fake_user).
    - Se parchea `get_db` para devolver una sesión simulada cuyo `query(...).filter(...).all()`
    devolverá la lista `fake_boards`.
    - Se realiza una petición GET a "/boards/" y se comprueba el status code 200.
    - Se valida que el JSON devuelto contiene los nombres esperados y que las
    llamadas a la sesión se realizaron (query -> filter -> all).
    """
    # Mock de usuario autenticado
    mock_get_user.return_value = fake_user

    # Mock de sesión/consulta a la DB
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

    ## Comprobamos que la respuesta contiene las boards simuladas
    mock_session.query.assert_called_once_with(Board)
    query_mock.filter.assert_called_once()
    filter_mock.all.assert_called_once()

# ----------------------------
# Test GET /boards/ sin boards
# ----------------------------
@patch("backend.boards.routers.get_db")
@patch("backend.boards.routers.get_current_user")
def test_get_boards_vacio(mock_get_user, mock_get_db):
    """
    Verifica que la ruta devuelva una lista vacía cuando el usuario no tiene boards.

    Flujo:
    - Se parchea `get_current_user` para devolver el usuario simulado.
    - Se parchea `get_db` para devolver una sesión simulada cuyo `query(...).filter(...).all()`
    devolverá una lista vacía.
    - Se realiza la petición GET y se comprueba que el cuerpo de la respuesta es [].
    """
    # Mock de usuario autenticado
    mock_get_user.return_value = fake_user

    # Mock de sesión que devuelve una lista vacía al consultar boards
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.all.return_value = []
    mock_get_db.return_value = mock_session

    # Ejecutar la ruta y comprobar que se recibe una lista vacía
    response = client.get("/boards/")
    assert response.status_code == 200
    data = response.json()
    assert data == []  # Lista vacía