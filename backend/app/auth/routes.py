"""
Endpoints de autenticación para NeoCare (registro y login de usuarios).

Este módulo implementa la funcionalidad para registrar nuevos usuarios
y autenticar el acceso mediante JWT, utilizando modelos y esquemas definidos.
"""
from fastapi import APIRouter, Depends, HTTPException, status   # 👈 IMPORTANTE
from sqlalchemy.orm import Session

from ..boards.models import User, Board, List
from ..auth.schemas import UserRegister, UserLogin, Token, UserOut
from ..auth.utils import hash_password, verify_password, create_token, get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Retorna los datos del usuario autenticado."""
    return current_user


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

    try:
        # 1) Crea el usuario con contraseña hasheada
        new_user = User(
            email=user.email,
            password_hash=hash_password(user.password),
            name=user.name,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        """
        NUEVO: crear tablero y listas por defecto para evitar que /boards/ devuelva [].

        - Crea 1 tablero "Tablero principal" asociado al usuario.
        - Crea 3 listas dentro del tablero, con position obligatorio (0,1,2).
        """

        # 2) Crea tablero por defecto
        default_board = Board(
            name="Tablero principal",
            user_id=new_user.id,
        )
        db.add(default_board)
        db.commit()
        db.refresh(default_board)

        # 3) Crea listas por defecto
        default_lists = [
            List(name="Por hacer", board_id=default_board.id, position=0),
            List(name="En curso", board_id=default_board.id, position=1),
            List(name="Hecho", board_id=default_board.id, position=2),
        ]
        db.add_all(default_lists)
        db.commit()

    except Exception as e:
        # ✅ Cambio: si algo falla en medio, no dejamos la BD "a medias"
        db.rollback()
        import traceback
        print(f"ERROR EN REGISTRO: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno creando usuario/tablero por defecto: {str(e)}",
        )

    # 4) Genera el JWT para el usuario recién creado
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