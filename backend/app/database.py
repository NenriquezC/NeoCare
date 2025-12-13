"""
Configura la conexión y manejo de la base de datos usando SQLAlchemy.

Este módulo establece el motor de la base de datos, la sesión local y la base
de declaración principal usada para definir modelos ORM. Por defecto, conecta
a una base PostgreSQL (los valores pueden sobrescribirse con la variable de entorno DATABASE_URL).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Extrae la URL de la base de datos desde la variable de entorno (o usa la URL por defecto)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:niki2025@localhost:5432/neocare_db"
)

# Crea el motor de conexión con SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=True  # Muestra las consultas SQL generadas (útil para desarrollo y depuración)
)

# Genera la clase de sesión para interactuar con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,           # Las transacciones no se confirman automáticamente
    autoflush=False,            # No se realiza autoflush en los cambios
    bind=engine                 # No se realiza autoflush en los cambios
)

# Clase base para los modelos ORM
Base = declarative_base()