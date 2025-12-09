# tests/test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, SessionLocal, engine, DATABASE_URL

# ----------------------------
# Test 1: Verificar que DATABASE_URL está definida
# ----------------------------
def test_database_url_definida():
    assert DATABASE_URL is not None
    assert DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("sqlite://")

# ----------------------------
# Test 2: Crear engine y session
# ----------------------------
def test_engine_y_session_local():
    assert engine is not None
    session = SessionLocal()
    assert session is not None
    session.close()

# ----------------------------
# Test 3: Crear base temporal en memoria (SQLite) para pruebas
# ----------------------------
def test_crear_tablas_temporales():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Verificar que se puede abrir y cerrar sesión
    db = TestSessionLocal()
    assert db is not None
    db.close()
