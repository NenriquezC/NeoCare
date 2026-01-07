import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

user_data = {"email": "test@example.com", "password": "password123", "name": "Test User"}
login_data = {"email": "test@example.com", "password": "password123"}
fake_token = "fake.jwt.token"

"""
Pruebas de integración para las rutas de autenticación (/auth/register y /auth/login).

Este módulo usa TestClient de FastAPI junto con la base de datos SQLite de testing
configurada en conftest.py.

Descripción general de las pruebas:
- test_register_success: registra un usuario nuevo cuando no existe el email en DB.
- test_register_existing_email: intenta registrar con un email ya existente y espera error 400.
- test_login_success: inicia sesión con credenciales válidas y devuelve un token.
- test_login_invalid_credentials: inicio de sesión con password inválida y devuelve 401.

Notas:
- Los tests usan el fixture 'client' de conftest.py que ya tiene configurada la BD SQLite.
- Cada test tiene una base de datos limpia gracias al fixture autouse de conftest.py.
"""
# ----------------------------
# Test /auth/register
# ----------------------------
@patch("app.auth.routes.hash_password")
@patch("app.auth.routes.create_token")
def test_register_success(mock_create_token, mock_hash_password, client):
    """Verifica el flujo de registro exitoso.

    Preparación:
    - Se usa el client fixture con base de datos SQLite limpia.
    - Se parchean hash_password y create_token para devolver valores controlados.

    Flujo:
    1. POST a /auth/register con user_data.
    2. Comprobar que la respuesta es 200 y contiene el token esperado.

    Aserciones:
    - status_code == 200
    - El JSON devuelto contiene access_token y token_type "bearer".
    """
    mock_hash_password.return_value = "hashed_password"
    mock_create_token.return_value = fake_token

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    assert response.json() == {
        "access_token": fake_token,
        "token_type": "bearer"
    }


def test_register_existing_email(client):
    """Verifica que registrar con un email ya existente devuelve error 400.

    Preparación:
    - Registra un usuario primero con el mismo email.

    Flujo:
    1. POST a /auth/register con user_data (primera vez - exitoso).
    2. POST a /auth/register con user_data (segunda vez - debe fallar).
    3. Comprobar que la respuesta es 400 con detalle "Email ya registrado".

    Aserciones:
    - status_code == 400
    - response.json()["detail"] == "Email ya registrado"
    """
    # Primer registro - debe ser exitoso
    client.post("/auth/register", json=user_data)
    
    # Segundo registro con el mismo email - debe fallar
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email ya registrado"


# ----------------------------
# Test /auth/login
# ----------------------------
def test_login_success(client):
    """Verifica el inicio de sesión exitoso y la emisión de un token.

    Preparación:
    - Registra un usuario primero.

    Flujo:
    1. POST a /auth/register para crear el usuario.
    2. POST a /auth/login con login_data.
    3. Comprobar que la respuesta es 200 y el JSON contiene access_token y token_type.

    Aserciones:
    - status_code == 200
    - JSON contiene "access_token" y "token_type": "bearer"
    """
    # Primero registrar el usuario
    client.post("/auth/register", json=user_data)
    
    # Ahora hacer login
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Verifica que credenciales inválidas retornan 401.

    Preparación:
    - Registra un usuario primero.

    Flujo:
    1. POST a /auth/register para crear usuario.
    2. POST a /auth/login con password incorrecta.
    3. Comprobar que la respuesta es 401 y el detalle indica credenciales incorrectas.

    Aserciones:
    - status_code == 401
    - response.json()["detail"] == "Credenciales incorrectas"
    """
    # Registrar usuario
    client.post("/auth/register", json=user_data)
    
    # Intentar login con password incorrecta
    invalid_login_data = {"email": "test@example.com", "password": "wrongpassword"}
    response = client.post("/auth/login", json=invalid_login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"
