import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import date, datetime
from decimal import Decimal

from app.main import app
from app.auth.utils import get_db, get_current_user
from app.boards.models import User, Card, TimeEntry, BoardMember

client = TestClient(app)

# Mock data
fake_user = User(id=1, email="test@example.com", name="Test User")
fake_board = MagicMock()
fake_board.user_id = 1
fake_card = Card(id=10, board_id=1, title="Test Card")
fake_card.board = fake_board
fake_membership = BoardMember(id=1, board_id=1, user_id=1)
fake_worklog = TimeEntry(
    id=100,
    user_id=1,
    card_id=10,
    date=date(2025, 1, 1),
    hours=Decimal("2.5"),
    note="Test note",
    created_at=datetime(2025, 1, 1, 10, 0, 0),
    updated_at=datetime(2025, 1, 1, 10, 0, 0)
)

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
# PRUEBAS FUNCIONALES
# ---------------------------------------------------------------------

def test_create_worklog_success(override_dependencies, mock_db):
    """✓ Crear un worklog válido"""
    mock_db.query.return_value.filter.return_value.first.side_effect = [fake_card, fake_membership]
    
    # Mock db.refresh to set the id and timestamps on the object
    def mock_refresh(obj):
        obj.id = 100
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
    
    mock_db.refresh.side_effect = mock_refresh
    
    payload = {
        "card_id": 10,
        "date": "2025-01-01",
        "hours": 2.5,
        "note": "Trabajando en la tarea"
    }
    
    response = client.post("/worklogs/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["card_id"] == 10
    assert float(data["hours"]) == 2.5

def test_create_worklog_zero_hours(override_dependencies):
    """✓ Crear un worklog con horas = 0 → rechazar"""
    payload = {
        "card_id": 10,
        "date": "2025-01-01",
        "hours": 0,
        "note": "Cero horas"
    }
    
    response = client.post("/worklogs/", json=payload)
    assert response.status_code == 422 # Unprocessable Entity (Pydantic validation)

def test_create_worklog_invalid_date(override_dependencies):
    """✓ Crear un worklog con fecha inválida → rechazar"""
    payload = {
        "card_id": 10,
        "date": "not-a-date",
        "hours": 2.0,
        "note": "Fecha mala"
    }
    
    response = client.post("/worklogs/", json=payload)
    assert response.status_code == 422

def test_update_worklog_success(override_dependencies, mock_db):
    """✓ Editar un worklog propio"""
    mock_db.query.return_value.filter.return_value.first.return_value = fake_worklog
    
    payload = {"hours": 5.0, "note": "Horas actualizadas"}
    response = client.put(f"/worklogs/{fake_worklog.id}", json=payload)
    
    assert response.status_code == 200
    assert float(response.json()["hours"]) == 5.0

def test_delete_worklog_success(override_dependencies, mock_db):
    """✓ Eliminar un worklog propio"""
    mock_db.query.return_value.filter.return_value.first.return_value = fake_worklog
    
    response = client.delete(f"/worklogs/{fake_worklog.id}")
    assert response.status_code == 204

def test_my_hours_summary(override_dependencies, mock_db):
    """✓ Ver totales correctos en vista “Mis horas”"""
    # Mocking the summary query
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_worklog]
    
    # Mocking the totals query (group by)
    mock_total = MagicMock()
    mock_total.date = date(2025, 1, 1)
    mock_total.total_hours = Decimal("2.5")
    
    # This is a bit tricky with MagicMock for complex queries
    # We'll mock the second query call
    mock_db.query.return_value.filter.return_value.group_by.return_value.all.return_value = [mock_total]
    
    response = client.get("/worklogs/me/week?week=2025-W01")
    
    assert response.status_code == 200
    data = response.json()
    assert float(data["total_hours"]) == 2.5
    assert len(data["entries"]) == 1

# ---------------------------------------------------------------------
# PRUEBAS DE SEGURIDAD
# ---------------------------------------------------------------------

def test_update_worklog_unauthorized(override_dependencies, mock_db):
    """✓ No permitir editar worklogs ajenos"""
    other_worklog = TimeEntry(id=101, user_id=99, card_id=10)
    mock_db.query.return_value.filter.return_value.first.return_value = other_worklog
    
    response = client.put("/worklogs/101", json={"hours": 1.0})
    assert response.status_code == 403
    assert response.json()["detail"] == "No autorizado"

def test_delete_worklog_unauthorized(override_dependencies, mock_db):
    """✓ No permitir eliminar worklogs ajenos"""
    other_worklog = TimeEntry(id=101, user_id=99, card_id=10)
    mock_db.query.return_value.filter.return_value.first.return_value = other_worklog
    
    response = client.delete("/worklogs/101")
    assert response.status_code == 403
    assert response.json()["detail"] == "No autorizado"

def test_endpoints_no_token():
    """✓ Probar endpoints sin token ( deben fallar )"""
    # We don't use override_dependencies here to test real security
    # But since we are using TestClient and dependency_overrides is global, 
    # we must ensure it's clear.
    app.dependency_overrides.clear()
    
    response = client.post("/worklogs/", json={})
    assert response.status_code == 401 # Unauthorized
