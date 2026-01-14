# tests/boards/test_routes.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""Pruebas de las rutas relacionadas con 'boards'.

Este módulo contiene pruebas que verifican el comportamiento de la ruta GET /boards/
utilizando TestClient de FastAPI y la base de datos de test configurada en conftest.py
"""

def test_get_boards_exitoso(client):
    """Verifica que GET /boards/ devuelve los tableros del usuario autenticado.

    Flujo de la prueba:
    1. Registrar un usuario.
    2. Autenticarse y obtener token.
    3. Verificar que se crea automáticamente un tablero por defecto.

    Aserciones / condiciones comprobadas:
    - El código de respuesta es 200 (OK).
    - El JSON devuelto contiene el tablero automático.
    """
    # Registrar usuario
    register_data = {
        "name": "Test User",
        "email": "testboards@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 200

    # Login para obtener token
    login_data = {
        "email": "testboards@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Obtener tableros: debe crear uno automáticamente
    response = client.get("/boards/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Tablero principal"

