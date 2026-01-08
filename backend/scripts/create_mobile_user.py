"""
Script para crear un usuario de prueba para la app móvil.

Uso:
    python create_mobile_user.py

Crea o actualiza el usuario movil@test.com con contraseña 123456
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.boards.models import User
from app.auth.utils import hash_password

# Configuración del usuario
USER_EMAIL = "movil@test.com"
USER_PASSWORD = "123456"
USER_NAME = "Usuario Movil"
USER_ROLE = "user"

db = SessionLocal()

# Datos del nuevo usuario
email = USER_EMAIL
password = USER_PASSWORD
name = USER_NAME

# Verificar si ya existe
existing = db.query(User).filter(User.email == email).first()

if existing:
    print(f"Usuario {email} ya existe. Actualizando contraseña...")
    existing.password_hash = hash_password(password)
    existing.name = name
    existing.role = USER_ROLE
    db.commit()
    print(f"✓ Usuario actualizado")
else:
    # Crear usuario nuevo
    new_user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
        role=USER_ROLE
    )
    db.add(new_user)
    db.commit()
    print(f"✓ Usuario creado: {email}")

print(f"\nCredenciales para la app móvil:")
print(f"  Email: {email}")
print(f"  Password: {password}")

db.close()
