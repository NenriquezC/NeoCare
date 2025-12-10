"""
tests/test_auth_routes.py
-------------------------

Pruebas para los endpoints de autenticación (/auth/register y /auth/login)
usando TestClient de FastAPI y mocks para aislar la lógica de persistencia y
los helpers de hashing/creación de tokens.

IMPORTANTE: Este archivo solo añade docstrings y comentarios explicativos sin
modificar la lógica ni el comportamiento original de las pruebas.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)

# Datos de ejemplo
user_data = {"email": "test@example.com", "password": "password123", "name": "Test User"}
login_data = {"email": "test@example.com", "password": "password123"}
fake_token = "fake.jwt.token"

# ----------------------------
# Test /auth/register
# ----------------------------
@patch("app.auth.routes.get_db")
@patch("app.auth.routes.hash_password")
@patch("app.auth.routes.create_token")
def test_register_success(mock_create_token, mock_hash_password, mock_get_db):
    """
    Registro exitoso de usuario.

    - Se parchea `get_db` para devolver una sesión simulada donde no existe el usuario.
    - Se parchea `hash_password` y `create_token` para controlar sus salidas.
    - Se realiza una petición POST a /auth/register con `user_data`.
    - Se comprueba que la respuesta contiene el token esperado y que la sesión DB
    recibió llamadas a `add` y `commit`.
    """
    # Mock de sesión de DB: simular que no existe un usuario con ese email
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = None  # No existe usuario
    mock_get_db.return_value = mock_session

    # Mock hash y token
    mock_hash_password.return_value = "hashed_password"
    mock_create_token.return_value = fake_token

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"access_token": fake_token, "token_type": "bearer"}

    # Verificar que la sesión DB recibió operaciones de persistencia
    mock_session.add.assert_called()  # Verifica que se llamó a add()
    mock_session.commit.assert_called()  # Verifica que se llamó a commit()

@patch("backend.auth.routes.get_db")
def test_register_existing_email(mock_get_db):
    """
    Registro fallido por email ya registrado.

    - Se parchea `get_db` para que la consulta indique que ya existe un usuario.
    - Se espera una respuesta 400 con detalle "Email ya registrado".
    """
    mock_session = MagicMock()
    # Simulamos que ya existe un usuario
    mock_session.query().filter().first.return_value = True
    mock_get_db.return_value = mock_session

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email ya registrado"

# ----------------------------
# Test /auth/login
# ----------------------------
@patch("app.auth.routes.get_db")
@patch("app.auth.routes.verify_password")
@patch("app.auth.routes.create_token")
def test_login_success(mock_create_token, mock_verify_password, mock_get_db):
    """
    Login exitoso con credenciales válidas.

    - Se parchea `get_db` para devolver un usuario simulado.
    - Se parchea `verify_password` para que valide la contraseña.
    - Se parchea `create_token` para devolver un token predefinido.
    - Se realiza POST a /auth/login y se comprueba el token en la respuesta.
    """
    mock_session = MagicMock()
    # Simulamos usuario existente en DB
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = user_data["email"]
    mock_user.password_hash = "hashed_password"
    mock_session.query().filter().first.return_value = mock_user
    mock_get_db.return_value = mock_session

    # Mock verify_password y create_token
    mock_verify_password.return_value = True
    mock_create_token.return_value = fake_token

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert response.json() == {"access_token": fake_token, "token_type": "bearer"}

@patch("app.auth.routes.get_db")
@patch("app.auth.routes.verify_password")
def test_login_invalid_credentials(mock_verify_password, mock_get_db):
    """
    Login fallido por credenciales inválidas.

    - Se parchea `get_db` para devolver un usuario existente.
    - Se parchea `verify_password` para que devuelva False, simulando contraseña incorrecta.
    - Se espera una respuesta 401 con detalle "Credenciales incorrectas".
    """
    mock_session = MagicMock()
    mock_user = MagicMock()
    mock_user.password_hash = "hashed_password"
    mock_session.query().filter().first.return_value = mock_user
    mock_get_db.return_value = mock_session

    # Simulamos contraseña incorrecta
    mock_verify_password.return_value = False

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"