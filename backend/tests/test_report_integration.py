import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta

from app.main import app
from app.database import Base
from app.auth.utils import get_db, get_current_user
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember

# Configuración de base de datos de prueba (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_report.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture
def setup_data():
    # Limpiar y poblar datos
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # 1. Crear usuario
    user = User(id=1, email="test@example.com", name="Test User", password_hash="...")
    db.add(user)
    
    # 2. Crear tablero
    board = Board(id=1, name="Test Board", user_id=1)
    db.add(board)
    
    # 3. Crear listas
    l_todo = List(id=1, board_id=1, name="Por hacer", position=0)
    l_done = List(id=5, board_id=1, name="Hecho", position=1)
    db.add(l_todo)
    db.add(l_done)
    
    # 4. Crear tarjetas
    # Semana 1 2026: 2025-12-29 al 2026-01-04
    
    # C1: Completada en la semana
    c1 = Card(id=10, board_id=1, list_id=5, title="Card 1", created_by_id=1,
              completed_at=datetime(2026, 1, 1), created_at=datetime(2025, 12, 1))
    # C2: Nueva en la semana
    c2 = Card(id=11, board_id=1, list_id=1, title="Card 2", created_by_id=1,
              created_at=datetime(2026, 1, 2))
    # C3: Vencida en la semana (y no en Hecho)
    c3 = Card(id=12, board_id=1, list_id=1, title="Card 3", created_by_id=1,
              due_date=date(2026, 1, 3), created_at=datetime(2025, 12, 1))
    
    db.add_all([c1, c2, c3])
    
    # 5. Crear Worklogs
    w1 = TimeEntry(user_id=1, card_id=10, date=date(2026, 1, 1), hours=5.0)
    w2 = TimeEntry(user_id=1, card_id=11, date=date(2026, 1, 2), hours=2.5)
    db.add_all([w1, w2])
    
    db.commit()
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: user
    
    yield db
    
    app.dependency_overrides.clear()
    db.close()

def test_report_integration_flow(setup_data):
    """✓ Integración: Flujo completo de informe con datos reales en DB"""
    
    # 1. Verificar Resumen
    response = client.get("/report/1/summary?week=2026-W01")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"]["count"] == 1
    assert data["new"]["count"] == 1
    assert data["overdue"]["count"] == 1
    
    # 2. Verificar Horas por Usuario
    response = client.get("/report/1/hours-by-user?week=2026-W01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total_hours"] == 7.5
    assert data[0]["tasks_count"] == 2
    
    # 3. Verificar Horas por Tarjeta
    response = client.get("/report/1/hours-by-card?week=2026-W01")
    assert response.status_code == 200
    data = response.json()
    # Debería haber 2 tarjetas con horas
    assert len(data) == 2
    assert data[0]["total_hours"] == 5.0
    assert data[1]["total_hours"] == 2.5

def test_report_integration_change_week(setup_data):
    """✓ Integración: Cambiar semana actualiza resultados"""
    # Semana 2 de 2026 (no hay datos)
    response = client.get("/report/1/summary?week=2026-W02")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"]["count"] == 0
    assert data["new"]["count"] == 0
    assert data["overdue"]["count"] == 0
    
    response = client.get("/report/1/hours-by-user?week=2026-W02")
    assert response.status_code == 200
    assert len(response.json()) == 0
