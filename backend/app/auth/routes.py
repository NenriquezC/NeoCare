"""
Endpoints de autenticación para NeoCare (registro y login de usuarios).

Este módulo implementa la funcionalidad para registrar nuevos usuarios
y autenticar el acceso mediante JWT, utilizando modelos y esquemas definidos.
"""
from fastapi import APIRouter, Depends, HTTPException, status   # 👈 IMPORTANTE
from sqlalchemy.orm import Session

from ..boards.models import User
from ..auth.schemas import UserRegister, UserLogin, Token
from ..auth.utils import hash_password, verify_password, create_token, get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Crea un usuario nuevo y retorna un token de acceso JWT.

    Parámetros:
        user (UserRegister): Datos de registro recibidos en el cuerpo de la petición.
        db (Session): Sesión de base de datos proporcionada por FastAPI.

    Retorna:
        Token: Diccionario con el JWT generado y el tipo de token.

    Excepciones:
        HTTP 400: Si el email ya está registrado en el sistema.
    """
    # Verifica si el correo ya está registrado
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado",
        )
    # Crea el usuario con contraseña hasheada
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        name=user.name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Genera el JWT para el usuario recién creado
    token = create_token({"user_id": new_user.id, "email": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica un usuario existente y retorna un token JWT si las credenciales son correctas.

    Parámetros:
        user (UserLogin): Credenciales enviadas por el cliente.
        db (Session): Sesión de base de datos proporcionada por FastAPI.

    Retorna:
        Token: Diccionario con el JWT generado y el tipo de token.

    Excepciones:
        HTTP 401: Si el email no existe o la contraseña no coincide.
    """
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    # Genera el JWT para el usuario autenticado
    token = create_token({"user_id": db_user.id, "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}