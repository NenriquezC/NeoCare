"""
tests/test_utils.py
-------------------

Pruebas unitarias para las utilidades de autenticación en app.auth.utils.

Este archivo añade docstrings y comentarios explicativos a las pruebas existentes
sin modificar su lógica ni su flujo. Las pruebas cubren:
- Hashing y verificación de contraseñas.
- Generación y decodificación de JWTs.
- Resolución del usuario actual a partir de un token (get_current_user),
incluyendo casos de token inválido y usuario inexistente.
"""
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
    """
    Comprueba que hash_password genera un hash distinto de la contraseña en claro
    y que verify_password valida correctamente la contraseña original y rechaza
    una contraseña errónea.
    """
    password = "mi_password_seguro"
    hashed = hash_password(password)
    assert hashed != password  # Debe estar hasheada
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_hash_password_none():
    """
    Verifica el comportamiento cuando se pasa None a hash_password.

    - Debe devolver una representación string.
    - verify_password debe comportarse de forma consistente (aquí se asume que
    None se normaliza a cadena vacía internamente).
    """
    hashed = hash_password(None)
    assert isinstance(hashed, str)
    assert verify_password("", hashed) is True  # None se convierte en ""

# =========================
# Tests create_token
# =========================
def test_create_token_contenido():
    """
    Genera un token con create_token y valida su contenido decodificándolo
    con la clave y el algoritmo esperados.

    Comprueba que los campos user_id y email se incluyan y que exista la
    reclamación 'exp' (expiración).
    """
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
    """
    Casos exitoso para get_current_user:

    - Se parchea jwt.decode para devolver un payload con user_id.
    - Se parchea SessionLocal para que la consulta a la DB devuelva un usuario simulado.
    - Se llama a get_current_user simulando la dependencia y se comprueba que
    se devuelve el usuario esperado y que jwt.decode fue invocado.
    """
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
    """
    Caso donde la decodificación del token falla (JWTError).

    - Se parchea jwt.decode para que lance JWTError.
    - Se espera que get_current_user lance una excepción con mensaje
    indicando token inválido o expirado.
    """
    # JWTError simulado
    with patch("app.auth.utils.jwt.decode", side_effect=JWTError):
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="bad.token", db=MagicMock())
        assert "Token inválido o expirado" in str(excinfo.value)

def test_get_current_user_usuario_no_existe():
    """
    Caso donde el token es válido pero la base de datos no devuelve un usuario.

    - Se parchea jwt.decode para devolver un payload con user_id.
    - Se parchea la sesión de DB para que la consulta devuelva None.
    - Se espera que get_current_user lance una excepción indicando token inválido
    o expirado (misma señalización usada por la implementación original).
    """
    # Token válido pero DB no devuelve usuario
    with patch("app.auth.utils.jwt.decode", return_value={"user_id": 1}):
        db_mock = MagicMock()
        db_mock.query().filter().first.return_value = None
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="fake.token", db=db_mock)
        assert "Token inválido o expirado" in str(excinfo.value)