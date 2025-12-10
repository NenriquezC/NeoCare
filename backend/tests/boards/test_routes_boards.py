# tests/boards/test_routes.py
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

from app.boards.models import Board
from app.main import app
from app.auth.utils import get_db, get_current_user

client = TestClient(app)

"""Pruebas de las rutas relacionadas con 'boards'.

Este módulo contiene pruebas que verifican el comportamiento de la ruta GET /boards/
utilizando TestClient de FastAPI y mocks para evitar dependencias externas (base de datos
y autenticación real).

Descripción y notas:
- Se simula un usuario autenticado sobrescribiendo la dependencia get_current_user.
- Se simula la sesión/consulta a la base de datos sobrescribiendo la dependencia get_db.
- Las pruebas esperan resultados deterministas usando objetos Board creados en memoria.
- Al final de cada prueba se limpia app.dependency_overrides para no afectar otras pruebas.
"""

def test_get_boards_exitoso():
    """Verifica que GET /boards/ devuelve los tableros del usuario autenticado.

    Flujo de la prueba:
    1. Crear un usuario falso (fake_user) con un id conocido.
    2. Construir una lista de Board (fake_boards) asociadas a ese usuario.
    3. Crear una sesión/ORM falsa (mock_session) cuyo .query(...).filter(...).all() devuelve fake_boards.
    4. Sobrescribir las dependencias de FastAPI:
    - get_current_user para que devuelva fake_user.
    - get_db para que rinda mock_session.
    5. Realizar una petición GET a /boards/ y validar la respuesta.

    Aserciones / condiciones comprobadas:
    - El código de respuesta es 200 (OK).
    - El JSON devuelto contiene exactamente los tableros esperados (longitud y nombres).
    - Se limpia app.dependency_overrides al final para restaurar el estado global.

    Consideraciones:
    - Se usa MagicMock para evitar acceso a una base de datos real.
    - Si la lógica de la ruta cambia (por ejemplo, paginación, serializadores distintos),
    es posible que haya que adaptar los asserts para comprobar campos adicionales o el formato.
    """
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