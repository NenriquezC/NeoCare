"""
Configuración global de pytest para todos los tests.

Este módulo configura:
- Base de datos SQLite para tests (evita problemas de encoding en Windows)
- Fixtures compartidas entre todos los tests
- Setup/teardown automático de la BD

IMPORTANTE: La variable TESTING=1 debe establecerse ANTES de importar app.database
para que use SQLite en lugar de PostgreSQL.
"""

import pytest
import os

# ⚠️ CRÍTICO: Establecer TESTING=1 ANTES de cualquier import de la app
# Esto hace que app.database.py use SQLite en lugar de PostgreSQL
os.environ["TESTING"] = "1"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine as app_engine
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember


# Usar el motor de la app que ya está configurado como SQLite (por TESTING=1)
# No necesitamos crear otro motor separado
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=app_engine  # Usar el engine de app.database que ya es SQLite en modo test
)


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """
    Crea las tablas antes de cada test y las elimina después.
    Esto garantiza que cada test tenga un estado limpio de la BD.
    """
    # Crear todas las tablas usando el engine de la app (SQLite en modo test)
    Base.metadata.create_all(bind=app_engine)
    
    yield
    
    # Limpiar después del test
    Base.metadata.drop_all(bind=app_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Proporciona una sesión de BD para un test.
    La sesión se hace rollback automáticamente después del test.
    """
    connection = app_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client():
    """
    Cliente de prueba de FastAPI configurado con la BD de test.
    """
    # Sobrescribir la dependencia de BD
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    from app.auth.utils import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar overrides
    app.dependency_overrides.clear()
