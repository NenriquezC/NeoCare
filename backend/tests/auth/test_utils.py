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

"""
Pruebas unitarias para las utilidades de autenticación (app.auth.utils).

Este módulo verifica:
- hash_password y verify_password: correcto hashing y verificación de contraseñas,
  incluyendo el caso en que se pase None.
- create_token: que el token JWT generado contiene el payload esperado y la
  reclamación de expiración ("exp").
- get_current_user: comportamiento ante token válido, token inválido/expirado,
  y cuando el usuario no existe en la base de datos.

Notas sobre implementaciones en las pruebas:
- Se usa patch/MagicMock para simular la decodificación JWT y la sesión de BD
  (SessionLocal) evitando dependencias externas.
- Las pruebas que simulan errores de JWT parchean jwt.decode para lanzar JWTError.
- Las pruebas esperan que get_current_user levante una excepción con mensaje
  apropiado cuando el token no es válido o el usuario no existe.
"""

# =========================
# Tests hash_password y verify_password
# =========================
def test_hash_y_verify_password():
    """Verifica que hash_password genera un hash distinto y que verify_password
    valida correctamente la contraseña original y niega contraseñas incorrectas.

    Comportamiento esperado:
    - El resultado de hash_password no debe ser igual a la contraseña en plano.
    - verify_password devuelve True para la contraseña correcta.
    - verify_password devuelve False para una contraseña incorrecta.
    """
    password = "mi_password_seguro"
    hashed = hash_password(password)
    assert hashed != password  # Debe estar hasheada
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_hash_password_none():
    """Verifica que pasar None a hash_password devuelve un string válido y que
    verify_password trata None (convertido a cadena vacía) de forma consistente.

    Comportamiento esperado:
    - hash_password(None) devuelve un str.
    - verify_password con cadena vacía y ese hash debe devolver True si la
      implementación normaliza None a "".
    """
    hashed = hash_password(None)
    assert isinstance(hashed, str)
    assert verify_password("", hashed) is True  # None se convierte en ""

# =========================
# Tests create_token
# =========================
def test_create_token_contenido():
    """Verifica que create_token incorpora correctamente el payload en el JWT.

    Comportamiento esperado:
    - El token decodificado contiene las claves del payload (user_id, email).
    - Contiene la reclamación 'exp' (expiración).
    - Se utiliza SECRET_KEY y ALGORITHM para decodificar el token.
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
    """Simula un token válido y una sesión de BD que devuelve un usuario.

    Preparación:
    - mock_jwt_decode devuelve un payload con 'user_id'.
    - mock_session_local y la sesión resultante devuelven un mock_user en la consulta.

    Comportamiento esperado:
    - get_current_user devuelve el usuario obtenido de la BD.
    - jwt.decode fue invocado para procesar el token.
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
    """Verifica que get_current_user lanza una excepción cuando el token es inválido.

    Preparación:
    - jwt.decode parcheado para lanzar JWTError.

    Comportamiento esperado:
    - Se lanza una excepción que contiene el mensaje indicativo de token inválido o expirado.
    """
    # JWTError simulado
    with patch("app.auth.utils.jwt.decode", side_effect=JWTError):
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="bad.token", db=MagicMock())
        assert "Token inválido o expirado" in str(excinfo.value)

def test_get_current_user_usuario_no_existe():
    """Verifica que get_current_user lanza excepción si el token es válido pero el usuario no existe.

    Preparación:
    - jwt.decode devuelve payload con 'user_id'.
    - la consulta a la BD devuelve None (usuario no encontrado).

    Comportamiento esperado:
    - Se lanza una excepción con mensaje indicando token inválido o expirado (o usuario no encontrado).
    """
    # Token válido pero DB no devuelve usuario
    with patch("app.auth.utils.jwt.decode", return_value={"user_id": 1}):
        db_mock = MagicMock()
        db_mock.query().filter().first.return_value = None
        with pytest.raises(Exception) as excinfo:
            get_current_user(token="fake.token", db=db_mock)
        assert "Token inválido o expirado" in str(excinfo.value)
