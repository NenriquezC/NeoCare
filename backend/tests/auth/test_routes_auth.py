import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)

user_data = {"email": "test@example.com", "password": "password123", "name": "Test User"}
login_data = {"email": "test@example.com", "password": "password123"}
fake_token = "fake.jwt.token"

"""
Pruebas de integración para las rutas de autenticación (/auth/register y /auth/login).

Este módulo usa TestClient de FastAPI junto con patch/MagicMock para simular dependencias
como la base de datos y las funciones de hashing/verificación de contraseñas y creación de tokens.

Descripción general de las pruebas:
- test_register_success: registra un usuario nuevo cuando no existe el email en DB.
- test_register_existing_email: intenta registrar con un email ya existente y espera error 400.
- test_login_success: inicia sesión con credenciales válidas y devuelve un token.
- test_login_invalid_credentials: inicio de sesión con password inválida y devuelve 401.

Notas:
- Algunas pruebas sobrescriben app.dependency_overrides temporalmente para inyectar sesiones falsas.
- Siempre limpiar app.dependency_overrides al final de la prueba que lo modifica para no afectar otras pruebas.
"""
# ----------------------------
# Test /auth/register
# ----------------------------
@patch("app.auth.routes.hash_password")
@patch("app.auth.routes.create_token")
def test_register_success(mock_create_token, mock_hash_password):
    """Verifica el flujo de registro exitoso.

    Preparación:
    - Se simula una sesión de DB (mock_session) cuya consulta no encuentra un usuario existente.
    - Se sobrescribe la dependencia get_db para devolver la mock_session.
    - Se parchean hash_password y create_token para devolver valores controlados.

    Flujo:
    1. POST a /auth/register con user_data.
    2. Comprobar que la respuesta es 200 y contiene el token esperado.

    Aserciones:
    - status_code == 200
    - El JSON devuelto contiene access_token y token_type "bearer".

    Consideraciones:
    - Se limpia app.dependency_overrides al final para restaurar el estado global.
    """
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # override real dependency
    from app.auth.utils import get_db
    def override_get_db():
        yield mock_session
    app.dependency_overrides[get_db] = override_get_db

    mock_hash_password.return_value = "hashed_password"
    mock_create_token.return_value = fake_token

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    assert response.json() == {
        "access_token": fake_token,
        "token_type": "bearer"
    }

    # Remove override so it doesn't affect other tests
    app.dependency_overrides.clear()


@patch("app.auth.utils.get_db")
def test_register_existing_email(mock_get_db):
    """Verifica que registrar con un email ya existente devuelve error 400.

    Preparación:
    - mock_get_db devuelve una sesión simulada cuya consulta encuentra un usuario existente.

    Flujo:
    1. POST a /auth/register con user_data.
    2. Comprobar que la respuesta es 400 con detalle "Email ya registrado".

    Aserciones:
    - status_code == 400
    - response.json()["detail"] == "Email ya registrado"
    """
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = True

    mock_get_db.return_value = iter([mock_session])

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email ya registrado"


# ----------------------------
# Test /auth/login
# ----------------------------
@patch("app.auth.utils.get_db")
@patch("app.auth.routes.verify_password")
@patch("app.auth.routes.create_token")
def test_login_success(mock_create_token, mock_verify_password, mock_get_db):
    """Verifica el inicio de sesión exitoso y la emisión de un token.

    Preparación:
    - Se crea una sesión simulada que devuelve un usuario con password_hash.
    - Se parchea verify_password para devolver True y create_token para devolver un token falso.

    Flujo:
    1. POST a /auth/login con login_data.
    2. Comprobar que la respuesta es 200 y el JSON contiene access_token y token_type.

    Aserciones:
    - status_code == 200
    - JSON == {"access_token": fake_token, "token_type": "bearer"}
    """
    mock_session = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = user_data["email"]
    mock_user.password_hash = "hashed_password"

    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_get_db.return_value = iter([mock_session])

    mock_verify_password.return_value = True
    mock_create_token.return_value = fake_token

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    assert response.json() == {"access_token": fake_token, "token_type": "bearer"}


@patch("app.auth.utils.get_db")
@patch("app.auth.routes.verify_password")
def test_login_invalid_credentials(mock_verify_password, mock_get_db):
    """Verifica que credenciales inválidas retornan 401.

    Preparación:
    - La sesión simulada devuelve un usuario pero verify_password se patcha para devolver False.

    Flujo:
    1. POST a /auth/login con login_data.
    2. Comprobar que la respuesta es 401 y el detalle indica credenciales incorrectas.

    Aserciones:
    - status_code == 401
    - response.json()["detail"] == "Credenciales incorrectas"
    """
    mock_session = MagicMock()
    mock_user = MagicMock()
    mock_user.password_hash = "hashed_password"

    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_get_db.return_value = iter([mock_session])

    mock_verify_password.return_value = False

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"
