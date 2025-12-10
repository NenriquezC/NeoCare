"""
Esquemas Pydantic para la gestión de autenticación en NeoCare.

Define los modelos de datos que se usan en las rutas de registro, login y respuestas 
de token JWT.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    """
    Esquema para recibir datos de registro de usuario.

    Campos:
        email (EmailStr): Correo electrónico válido.
        password (str): Contraseña del usuario.
        name (str, opcional): Nombre del usuario.
    """
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """
    Esquema para datos de login (inicio de sesión).

    Campos:
        email (EmailStr): Correo electrónico válido.
        password (str): Contraseña del usuario.
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Esquema de respuesta para el token JWT.

    Campos:
        access_token (str): Token de acceso generado.
        token_type (str): Tipo de autenticación (bearer por defecto).
    """
    access_token: str
    token_type: str = "bearer"