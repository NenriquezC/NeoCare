# tests/auth/test_schemas.py
import pytest
from pydantic import ValidationError
from app.auth.schemas import UserRegister, UserLogin, Token

"""
Pruebas para los esquemas de autenticación (Pydantic) en app.auth.schemas.

Este módulo valida:
- UserRegister: creación válida, campos opcionales y validación de email.
- UserLogin: creación válida y validación de email.
- Token: presencia del campo access_token y comportamiento del campo token_type por defecto y personalizado.

Las pruebas usan pytest y comprueban tanto casos válidos como errores de validación
lanzados por Pydantic (ValidationError).
"""

# ----------------------------
# Tests UserRegister
# ----------------------------
def test_user_register_valido():
    """Comprueba que UserRegister acepta datos válidos.

    Flujo:
    1. Crear instancia UserRegister con email, password y name válidos.
    2. Comprobar que los atributos se asignan correctamente.

    Aserciones:
    - user.email, user.password y user.name coinciden con los valores proporcionados.
    """
    user = UserRegister(email="test@example.com", password="password123", name="Test User")
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.name == "Test User"

def test_user_register_sin_name():
    """Verifica que el campo `name` es opcional en UserRegister.

    Flujo:
    1. Crear instancia UserRegister sin proporcionar `name`.
    2. Comprobar que el campo `name` queda en None por defecto.

    Aserciones:
    - user.name es None cuando no se suministra.
    """
    user = UserRegister(email="user2@example.com", password="password123")
    assert user.name is None  # El campo opcional debe ser None por defecto

def test_user_register_email_invalido():
    """Asegura que UserRegister valida el formato de email usando Pydantic.

    Flujo:
    1. Intentar crear UserRegister con un email inválido.
    2. Esperar que Pydantic lance ValidationError.

    Aserciones:
    - Se lanza ValidationError para emails con formato incorrecto.
    """
    with pytest.raises(ValidationError):
        UserRegister(email="correo-invalido", password="password123", name="Test User")

# ----------------------------
# Tests UserLogin
# ----------------------------
def test_user_login_valido():
    """Comprueba que UserLogin acepta credenciales válidas.

    Flujo:
    1. Crear instancia UserLogin con email y password válidos.
    2. Verificar los atributos resultantes.

    Aserciones:
    - user.email y user.password coinciden con los valores proporcionados.
    """
    user = UserLogin(email="login@example.com", password="password123")
    assert user.email == "login@example.com"
    assert user.password == "password123"

def test_user_login_email_invalido():
    """Verifica que UserLogin valida el formato de email y lanza ValidationError si es inválido.

    Flujo:
    1. Intentar crear UserLogin con email mal formado.
    2. Esperar ValidationError de Pydantic.

    Aserciones:
    - Se lanza ValidationError para el email inválido.
    """
    with pytest.raises(ValidationError):
        UserLogin(email="login-invalido", password="password123")

# ----------------------------
# Tests Token
# ----------------------------
def test_token_valido():
    """Comprueba la creación de Token con valores por defecto.

    Flujo:
    1. Crear Token con access_token.
    2. Verificar que access_token se asigna y token_type toma el valor por defecto.

    Aserciones:
    - token.access_token coincide con el valor proporcionado.
    - token.token_type es 'bearer' por defecto.
    """
    token = Token(access_token="fake.jwt.token")
    assert token.access_token == "fake.jwt.token"
    assert token.token_type == "bearer"  # Valor por defecto

def test_token_tipo_personalizado():
    """Verifica que Token acepta un token_type personalizado.

    Flujo:
    1. Crear Token indicando token_type distinto al por defecto.
    2. Comprobar que el token_type se guarda correctamente.

    Aserciones:
    - token.token_type coincide con el valor personalizado pasado.
    """
    token = Token(access_token="fake.jwt.token", token_type="custom")
    assert token.token_type == "custom"
