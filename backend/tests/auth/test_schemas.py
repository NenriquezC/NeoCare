# tests/auth/test_schemas.py
import pytest
from pydantic import ValidationError
from app.auth.schemas import UserRegister, UserLogin, Token

# ----------------------------
# Tests UserRegister
# ----------------------------
def test_user_register_valido():
    user = UserRegister(email="test@example.com", password="password123", name="Test User")
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.name == "Test User"

def test_user_register_sin_name():
    user = UserRegister(email="user2@example.com", password="password123")
    assert user.name is None  # El campo opcional debe ser None por defecto

def test_user_register_email_invalido():
    with pytest.raises(ValidationError):
        UserRegister(email="correo-invalido", password="password123", name="Test User")

# ----------------------------
# Tests UserLogin
# ----------------------------
def test_user_login_valido():
    user = UserLogin(email="login@example.com", password="password123")
    assert user.email == "login@example.com"
    assert user.password == "password123"

def test_user_login_email_invalido():
    with pytest.raises(ValidationError):
        UserLogin(email="login-invalido", password="password123")

# ----------------------------
# Tests Token
# ----------------------------
def test_token_valido():
    token = Token(access_token="fake.jwt.token")
    assert token.access_token == "fake.jwt.token"
    assert token.token_type == "bearer"  # Valor por defecto

def test_token_tipo_personalizado():
    token = Token(access_token="fake.jwt.token", token_type="custom")
    assert token.token_type == "custom"
