from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..boards.models import User  # tu modelo User está ahí


# ===== CONFIG JWT =====
SECRET_KEY = "CAMBIA_ESTA_CLAVE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ===== CONTRASEÑAS =====
def hash_password(password: str) -> str:
    """
    Hashea la contraseña usando bcrypt.
    Bcrypt sólo admite hasta 72 bytes, así que truncamos por seguridad.
    """
    if password is None:
        password = ""
    #password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica la contraseña en texto plano contra el hash almacenado.
    Aplicamos el mismo truncado que en hash_password.
    """
    if plain is None:
        plain = ""
    #plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# ===== TOKEN: CREAR =====
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ===== DEPENDENCIA DB =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TOKEN: VALIDAR Y OBTENER USUARIO
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
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