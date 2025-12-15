"""
Utilidades de autenticación y gestión de usuarios para el backend NeoCare.

Incluye funciones de hashing y verificación de contraseñas, generación y validación
de tokens JWT, y dependencias para obtener usuarios autenticados y la sesión de base
de datos.
"""
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..boards.models import User  # tu modelo User está ahí


# ======== CONFIGURACIÓN DE JWT =========
SECRET_KEY = "CAMBIA_ESTA_CLAVE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ===== CONTRASEÑAS =====
def hash_password(password: str) -> str:
    """
    Hashea la contraseña del usuario utilizando el algoritmo pbkdf2_sha256.

    Args:
        password (str): Contraseña original en texto plano.

    Returns:
        str: Contraseña encriptada/hasheada.
    """
    if password is None:
        password = ""
    #password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica que la contraseña en texto plano coincida con el hash almacenado.

    Args:
        plain (str): Contraseña en texto plano proporcionada por el usuario.
        hashed (str): Contraseña hasheada almacenada en la base de datos.

    Returns:
        bool: True si coincide, False si no.
    """
    if plain is None:
        plain = ""
    #plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# ===== TOKEN: CREAR =====
def create_token(data: dict):
    """
    Genera un token JWT codificando los datos de usuario.

    Args:
        data (dict): Datos a incluir en el payload del token.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ===== DEPENDENCIA DB =====
def get_db():
    """
    Genera una sesión nueva de base de datos para inyectar en rutas de FastAPI.

    Yields:
        Session: Sesión SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TOKEN: VALIDAR Y OBTENER USUARIO
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual autenticado a partir del token JWT.

    Args:
        token (str): Token JWT extraído automáticamente por FastAPI.
        db (Session): Sesión SQLAlchemy, inyectada.

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe.

    Returns:
        User: Instancia del usuario autenticado en base de datos.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_error

    return user