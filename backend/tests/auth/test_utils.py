# tests/auth/test_utils.py
import pytest
from unittest.mock import patch, MagicMock
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.auth.utils import (
    hash_password,
    verify_password,
    create_token,
    get_current_user,
    SECRET_KEY,
    ALGORITHM,
)

# =========================
# Tests hash_password y verify_password
# =========================
def test_hash_y_verify_password():
    password = "mi_password_seguro"
    hashed = hash_password(password)
    assert hashed != password  # Debe estar hasheada
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_hash_password_none():
    hashed = hash_password(None)
    assert isinstance(hashed, str)
    assert verify_password("", hashed) is True  # None se convierte en ""

# =========================
# Tests create_token
# =========================
def test_create_token_contenido():
    data = {"user_id": 1, "email": "test@example.com"}
    token = create_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["user_id"] == 1
    assert decoded["email"] == "test@example.com"
    assert "exp" in decoded

# =========================
# Test get_current_user
# =========================
@patch("app.auth.utils.SessionLocal")
@patch("app.auth.utils.jwt.decode")
def test_get_current_user_exitoso(mock_jwt_decode, mock_session_local):
    # Mock del payload decodificado
    mock_jwt_decode.return_value = {"user_id": 1}

    # Mock de la DB
    mock_user = MagicMock()
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = mock_user
    mock_session_local.return_value = mock_session

    # Llamada directa simulando dependencia FastAPI
    user = get_current_user(token="fake.token", db=mock_session)
    assert user == mock_user
    mock_jwt_decode.assert_called_once()

def test_get_current_user_token_invalido():
    # JWTError simulado
    with patch("app.auth.utils.jwt.decode", side_effect=JWTError):
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="bad.token", db=MagicMock())
        assert "Token inválido o expirado" in str(excinfo.value)

def test_get_current_user_usuario_no_existe():
    # Token válido pero DB no devuelve usuario
    with patch("app.auth.utils.jwt.decode", return_value={"user_id": 1}):
        db_mock = MagicMock()
        db_mock.query().filter().first.return_value = None
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="fake.token", db=db_mock)
        assert "Token inválido o expirado" in str(excinfo.value)
