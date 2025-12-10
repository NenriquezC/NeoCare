"""
test_database.py
----------------

Pruebas unitarias para la capa de base de datos de la aplicación.

Estas pruebas verifican:
- Que la URL de la base de datos esté definida y tenga un esquema esperado.
- Que el engine y el factory de sesiones (SessionLocal) estén disponibles.
- Que se puedan crear tablas temporales en una base de datos SQLite en memoria
y abrir/cerrar sesiones sobre ella.

Notas:
- Estas pruebas son rápidas y aisladas; la creación de tablas en memoria permite
ejecutar verificaciones sin tocar la base de datos real.
- En entornos CI/integación puede considerarse el uso de fixtures más completas
que apliquen migraciones y limpien el estado entre pruebas.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, SessionLocal, engine, DATABASE_URL


def test_database_url_definida():
    """
    Verifica que la configuración de la aplicación exponga una URL de base de datos.

    Comprueba:
    - Que DATABASE_URL no sea None.
    - Que el esquema sea uno de los esperados (postgresql:// o sqlite://).

    Propósito:
    - Detectar problemas de configuración antes de que otras pruebas que dependan
    de la base de datos sean ejecutadas.
    """
    assert DATABASE_URL is not None
    assert DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("sqlite://")


def test_engine_y_session_local():
    """
    Comprueba que el engine y la fábrica de sesiones están disponibles.

    Pasos:
    - Verificar que el objeto `engine` exportado por app.database no sea None.
    - Crear una sesión con `SessionLocal()` y cerrarla correctamente.

    Propósito:
    - Validar la configuración básica de SQLAlchemy usada por la aplicación.
    """
    assert engine is not None
    session = SessionLocal()
    assert session is not None
    session.close()


def test_crear_tablas_temporales():
    """
    Crea un engine SQLite en memoria y registra las tablas definidas en `Base`.

    Pasos:
    1. Crear un engine con sqlite:///:memory: para aislamiento total.
    2. Crear un SessionLocal ligado a ese engine.
    3. Ejecutar Base.metadata.create_all() para crear las tablas en memoria.
    4. Abrir y cerrar una sesión para validar que la configuración funciona.

    Propósito:
    - Asegurar que las definiciones de modelos (Base) son correctas y que pueden
    materializarse en una base de datos real sin errores de metadatos.
    - Esta prueba no valida migraciones ni integridad de datos, solo la capacidad
    de crear la estructura definida por los modelos.
    """

    # Engine SQLite en memoria para pruebas aisladas y rápidas
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(bind=test_engine)

    # Crear las tablas definidas por los modelos importados en Base
    Base.metadata.create_all(bind=test_engine)

    # Verificar que se puede abrir y cerrar una sesión sobre el engine en memoria
    db = TestSessionLocal()
    assert db is not None
    db.close()