
from fastapi.testclient import TestClient
from tests.conftest import TestingSessionLocal
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember
import uuid
from datetime import date, timedelta
import pytest

def crear_usuario_y_token(client):
    email = f"test_{uuid.uuid4().hex}@example.com"
    payload = {
        "email": email,
        "password": "password123",
        "name": "Tester",
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    token = data["access_token"]
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user, token

def preparar_escenario(client):
    user, token = crear_usuario_y_token(client)
    db = TestingSessionLocal()
    board = Board(name="Test Board", user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)
    
    # Add user as member
    member = BoardMember(board_id=board.id, user_id=user.id, role="owner")
    db.add(member)
    
    lst = List(name="Test List", board_id=board.id, position=0)
    db.add(lst)
    db.commit()
    db.refresh(lst)
    
    card = Card(title="Test Card", board_id=board.id, list_id=lst.id, created_by_id=user.id)
    db.add(card)
    db.commit()
    db.refresh(card)
    
    card_id = card.id
    db.close()
    return user, token, card_id

def test_create_worklog_success(client):
    user, token, card_id = preparar_escenario(client)
    payload = {
        "card_id": card_id,
        "date": str(date.today()),
        "hours": 2.5,
        "note": "Trabajando en el test"
    }
    resp = client.post("/worklogs/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["hours"] == "2.50"
    assert data["note"] == "Trabajando en el test"

def test_create_worklog_invalid_hours(client):
    user, token, card_id = preparar_escenario(client)
    payload = {
        "card_id": card_id,
        "date": str(date.today()),
        "hours": 0,
        "note": "Cero horas"
    }
    resp = client.post("/worklogs/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422 # Pydantic validation error

def test_create_worklog_future_date(client):
    user, token, card_id = preparar_escenario(client)
    payload = {
        "card_id": card_id,
        "date": str(date.today() + timedelta(days=1)),
        "hours": 1,
        "note": "Futuro"
    }
    resp = client.post("/worklogs/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400
    assert "futuras" in resp.json()["detail"]

def test_list_worklogs(client):
    user, token, card_id = preparar_escenario(client)
    # Create one
    client.post("/worklogs/", json={"card_id": card_id, "date": str(date.today()), "hours": 1}, headers={"Authorization": f"Bearer {token}"})
    
    resp = client.get(f"/worklogs/card/{card_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

def test_update_worklog_own(client):
    user, token, card_id = preparar_escenario(client)
    resp_create = client.post("/worklogs/", json={"card_id": card_id, "date": str(date.today()), "hours": 1}, headers={"Authorization": f"Bearer {token}"})
    worklog_id = resp_create.json()["id"]
    
    resp_update = client.put(f"/worklogs/{worklog_id}", json={"hours": 5, "note": "Updated"}, headers={"Authorization": f"Bearer {token}"})
    assert resp_update.status_code == 200
    assert resp_update.json()["hours"] == "5.00"
    assert resp_update.json()["note"] == "Updated"

def test_update_worklog_other_user(client):
    user1, token1, card_id = preparar_escenario(client)
    resp_create = client.post("/worklogs/", json={"card_id": card_id, "date": str(date.today()), "hours": 1}, headers={"Authorization": f"Bearer {token1}"})
    worklog_id = resp_create.json()["id"]
    
    user2, token2 = crear_usuario_y_token(client)
    # User 2 is not even in the board, but even if they were, they shouldn't edit user 1's worklog
    resp_update = client.put(f"/worklogs/{worklog_id}", json={"hours": 5}, headers={"Authorization": f"Bearer {token2}"})
    assert resp_update.status_code == 403

def test_delete_worklog_own(client):
    user, token, card_id = preparar_escenario(client)
    resp_create = client.post("/worklogs/", json={"card_id": card_id, "date": str(date.today()), "hours": 1}, headers={"Authorization": f"Bearer {token}"})
    worklog_id = resp_create.json()["id"]
    
    resp_delete = client.delete(f"/worklogs/{worklog_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp_delete.status_code == 204

def test_my_hours_week(client):
    user, token, card_id = preparar_escenario(client)
    today = date.today()
    # Get ISO week
    year, week_num, _ = today.isocalendar()
    week_str = f"{year}-W{week_num:02d}"
    
    client.post("/worklogs/", json={"card_id": card_id, "date": str(today), "hours": 3}, headers={"Authorization": f"Bearer {token}"})
    
    resp = client.get(f"/worklogs/me/week?week={week_str}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["week"] == week_str
    assert float(data["total_hours"]) >= 3
    assert len(data["entries"]) >= 1
