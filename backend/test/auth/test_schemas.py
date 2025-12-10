"""
tests/test_schemas.py
---------------------

Pruebas unitarias para los esquemas (Pydantic) del módulo de autenticación.

Este archivo añade docstrings y comentarios explicativos a cada prueba sin
modificar la lógica ni las aserciones originales. Las pruebas verifican:
- Validez y comportamiento por defecto de UserRegister, UserLogin y Token.
- Manejo de errores de validación (ValidationError) para correos inválidos.
"""
import pytest
from pydantic import ValidationError
from app.auth.schemas import UserRegister, UserLogin, Token

# ----------------------------
# Tests UserRegister
# ----------------------------
def test_user_register_valido():
    """
    Verifica que la creación de un UserRegister con datos válidos funcione.

    - Crea una instancia con email, password y name.
    - Comprueba que los atributos contienen los valores proporcionados.
    """
    user = UserRegister(email="test@example.com", password="password123", name="Test User")
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.name == "Test User"

def test_user_register_sin_name():
    """
    Verifica el comportamiento cuando el campo `name` es omitido.

    - `name` es opcional en el esquema; al no proporcionarlo, debe ser None.
    """
    user = UserRegister(email="user2@example.com", password="password123")
    assert user.name is None  # El campo opcional debe ser None por defecto

def test_user_register_email_invalido():
    """
    Asegura que un email inválido lance un ValidationError.

    - Proporciona un email con formato inválido y espera que Pydantic valide y
    arroje ValidationError.
    """
    with pytest.raises(ValidationError):
        UserRegister(email="correo-invalido", password="password123", name="Test User")

# ----------------------------
# Tests UserLogin
# ----------------------------
def test_user_login_valido():
    """
    Verifica que UserLogin acepte datos válidos.

    - Crea una instancia con email y password y comprueba los atributos.
    """
    user = UserLogin(email="login@example.com", password="password123")
    assert user.email == "login@example.com"
    assert user.password == "password123"

def test_user_login_email_invalido():
    """
    Asegura que un email inválido en UserLogin lance ValidationError.
    """
    with pytest.raises(ValidationError):
        UserLogin(email="login-invalido", password="password123")

# ----------------------------
# Tests Token
# ----------------------------
def test_token_valido():
    """
    Verifica la creación de un Token con el comportamiento por defecto.

    - Si no se especifica `token_type`, el valor por defecto debe ser "bearer".
    """
    token = Token(access_token="fake.jwt.token")
    assert token.access_token == "fake.jwt.token"
    assert token.token_type == "bearer"  # Valor por defecto

def test_token_tipo_personalizado():
    """
    Comprueba que `token_type` se puede personalizar al instanciar Token.
    """
    token = Token(access_token="fake.jwt.token", token_type="custom")
    assert token.token_type == "custom"