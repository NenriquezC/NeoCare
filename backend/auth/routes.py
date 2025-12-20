from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app import models
from app.auth.schemas import UserRegister, UserLogin, UserOut, Token
from app.auth.utils import hash_password, verify_password, create_token, verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter()

# ---------- REGISTER ----------
@auth_router.post("/register", response_model=UserOut)
def register(user: UserRegister, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")

    hashed = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------- LOGIN ----------
@auth_router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

# ---------- GET CURRENT USER ----------
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
