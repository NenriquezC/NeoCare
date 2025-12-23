"""
Pruebas relacionadas con la configuración y el acceso a la capa de persistencia (app.database).

Este módulo verifica:
- Que la URL de la base de datos (DATABASE_URL) esté definida y tenga un esquema esperado.
- Que el engine y SessionLocal expuestos por app.database se puedan instanciar.
- Que se puedan crear tablas en una base de datos SQLite en memoria y abrir/cerrar una sesión.

Estas pruebas son ligeras y no requieren una base de datos externa configurada; la tercera prueba utiliza
un engine SQLite en memoria para validar la creación de metadatos y la apertura de sesiones.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, SessionLocal, engine, DATABASE_URL

# ----------------------------
# Test 1: Verificar que DATABASE_URL está definida
# ----------------------------
def test_database_url_definida():
    """Comprueba que la configuración expone DATABASE_URL y que tiene un esquema plausible.

    Aserciones:
    - DATABASE_URL no es None.
    - El valor comienza con 'postgresql://' o 'sqlite://', esquemas esperados en la aplicación.
    """
    assert DATABASE_URL is not None
    assert DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("sqlite://")

# ----------------------------
# Test 2: Crear engine y session
# ----------------------------
def test_engine_y_session_local():
    """Verifica que el engine y SessionLocal exportados por app.database son utilizables.

    Flujo:
    1. Comprueba que `engine` está definido.
    2. Intenta crear una sesión usando SessionLocal y cerrar la sesión.

    Aserciones:
    - `engine` no es None.
    - La sesión creada por SessionLocal se puede instanciar y cerrar sin errores.
    """
    assert engine is not None
    session = SessionLocal()
    assert session is not None
    session.close()

# ----------------------------
# Test 3: Crear base temporal en memoria (SQLite) para pruebas
# ----------------------------
def test_crear_tablas_temporales():
    """Crea un engine SQLite en memoria, genera las tablas definidas en Base y abre una sesión.

    Flujo:
    1. Crear un engine SQLite en memoria y un sessionmaker ligado a él.
    2. Llamar a Base.metadata.create_all(bind=test_engine) para crear las tablas.
    3. Abrir y cerrar una sesión para verificar que la configuración de metadatos y conexión funciona.

    Aserciones:
    - Se puede instanciar y cerrar una sesión sobre la base temporal sin errores.
    """
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Verificar que se puede abrir y cerrar sesión
    db = TestSessionLocal()
    assert db is not None
    db.close()
