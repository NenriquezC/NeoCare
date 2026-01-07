"""
Configura la conexión y manejo de la base de datos usando SQLAlchemy.

Este módulo establece el motor de la base de datos, la sesión local y la base
de declaración principal usada para definir modelos ORM. Por defecto, conecta
a una base PostgreSQL (los valores pueden sobrescribirse con la variable de entorno DATABASE_URL).

En modo TEST (cuando TESTING=1), usa SQLite para evitar problemas de encoding en Windows.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
from pathlib import Path

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    # Buscar el archivo .env en el directorio backend
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # Si python-dotenv no está instalado, continuar sin él
    pass

# Detectar si estamos en modo test
IS_TESTING = os.getenv("TESTING", "0") == "1"

if IS_TESTING:
    # Modo TEST: Usar SQLite (sin problemas de encoding en Windows)
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        DATABASE_URL,
        future=True,
        echo=False,  # No mostrar SQL en tests (menos ruido)
        connect_args={"check_same_thread": False}  # Necesario para SQLite
    )
else:
    # Modo PRODUCCIÓN/DESARROLLO: Usar PostgreSQL
    # Forzar codificación UTF-8 en Windows
    if sys.platform == 'win32':
        os.environ['PGCLIENTENCODING'] = 'UTF8'
    
    # Extrae la URL de la base de datos desde la variable de entorno (o usa la URL por defecto)
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:niki2025@localhost:5432/neocare_db_2"
    )
    
    # Crea el motor de conexión con SQLAlchemy
    engine = create_engine(
        DATABASE_URL,
        future=True,
        echo=True,  # Muestra las consultas SQL generadas (útil para desarrollo y depuración)
        connect_args={"client_encoding": "UTF8", "options": "-c client_encoding=UTF8"},
        pool_pre_ping=True  # Verifica la conexión antes de usarla
    )

# Genera la clase de sesión para interactuar con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,           # Las transacciones no se confirman automáticamente
    autoflush=False,            # No se realiza autoflush en los cambios
    bind=engine                 # No se realiza autoflush en los cambios
)

# Clase base para los modelos ORM
Base = declarative_base()