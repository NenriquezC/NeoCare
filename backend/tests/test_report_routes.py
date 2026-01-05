import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import date, datetime
from decimal import Decimal

from app.main import app
from app.auth.utils import get_db, get_current_user
from app.boards.models import User, Card, Board, List, BoardMember

client = TestClient(app)

# Mock data
fake_user = User(id=1, email="test@example.com", name="Test User")
fake_board = Board(id=1, user_id=1, name="Test Board")
fake_list_done = List(id=5, board_id=1, name="Hecho")

@pytest.fixture
def mock_db():
    mock = MagicMock()
    yield mock

@pytest.fixture
def override_dependencies(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield
    app.dependency_overrides.clear()

# ---------------------------------------------------------------------
# PRUEBAS DE RESUMEN SEMANAL
# ---------------------------------------------------------------------

def test_get_weekly_summary_success(override_dependencies, mock_db):
    """✓ Resumen semanal: calcular completadas, nuevas y vencidas"""
    # Mock verify_board_access (Board query)
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        fake_board,      # verify_board_access -> Board
        fake_list_done   # get_weekly_summary -> List "Hecho"
    ]
    
    # Mock cards
    c1 = Card(id=10, board_id=1, title="Completada", list_id=5, 
              completed_at=datetime(2026, 1, 1), created_at=datetime(2025, 12, 1))
    c2 = Card(id=11, board_id=1, title="Nueva", list_id=1, 
              created_at=datetime(2026, 1, 2))
    c3 = Card(id=12, board_id=1, title="Vencida", list_id=1, 
              due_date=date(2026, 1, 3), created_at=datetime(2025, 12, 1))
    
    mock_db.query.return_value.filter.return_value.all.return_value = [c1, c2, c3]
    
    # Semana 1 de 2026 (2025-12-29 al 2026-01-04)
    response = client.get("/report/1/summary?week=2026-W01")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["completed"]["count"] == 1
    assert data["completed"]["items"][0]["title"] == "Completada"
    
    assert data["new"]["count"] == 1
    assert data["new"]["items"][0]["title"] == "Nueva"
    
    assert data["overdue"]["count"] == 1
    assert data["overdue"]["items"][0]["title"] == "Vencida"

# ---------------------------------------------------------------------
# PRUEBAS DE HORAS
# ---------------------------------------------------------------------

def test_get_hours_by_user_success(override_dependencies, mock_db):
    """✓ Horas por usuario: verificar agregación mockeada"""
    mock_db.query.return_value.filter.return_value.first.return_value = fake_board
    
    # Mock result of the complex query
    mock_row = MagicMock()
    mock_row.user_id = 1
    mock_row.user_name = "Test User"
    mock_row.total_hours = 10.5
    mock_row.tasks_count = 2
    
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.group_by.return_value.all.return_value = [mock_row]
    
    response = client.get("/report/1/hours-by-user?week=2026-W01")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total_hours"] == 10.5
    assert data[0]["tasks_count"] == 2

def test_get_hours_by_card_success(override_dependencies, mock_db):
    """✓ Horas por tarjeta: verificar orden y datos"""
    mock_db.query.return_value.filter.return_value.first.return_value = fake_board
    
    mock_row = MagicMock()
    mock_row.card_id = 10
    mock_row.title = "Test Card"
    mock_row.responsible = "Test User"
    mock_row.status = "En progreso"
    mock_row.total_hours = 5.0
    
    # Mock query chain
    mock_db.query.return_value.join.return_value.join.return_value.outerjoin.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [mock_row]
    
    response = client.get("/report/1/hours-by-card?week=2026-W01")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total_hours"] == 5.0
    assert data[0]["title"] == "Test Card"

# ---------------------------------------------------------------------
# PRUEBAS DE SEGURIDAD
# ---------------------------------------------------------------------

def test_get_report_unauthorized(override_dependencies, mock_db):
    """✓ Seguridad: No permitir acceso a tableros ajenos"""
    # Board belongs to user 99
    other_board = Board(id=1, user_id=99, name="Other Board")
    
    # verify_board_access -> Board query returns other_board
    # verify_board_access -> BoardMember query returns None
    mock_db.query.return_value.filter.return_value.first.side_effect = [other_board, None]
    
    response = client.get("/report/1/summary?week=2026-W01")
    
    assert response.status_code == 403
    assert "No tienes acceso" in response.json()["detail"]

def test_get_report_no_jwt():
    """✓ Seguridad: JWT obligatorio (sin override)"""
    # No override_dependencies fixture here
    response = client.get("/report/1/summary?week=2026-W01")
    assert response.status_code == 401
