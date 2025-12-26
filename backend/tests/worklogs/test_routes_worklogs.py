from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime, date, timezone, timedelta
from app.main import app
from app.auth.utils import get_db, get_current_user
from app.boards.models import User, Card, Board, TimeEntry, BoardMember

client = TestClient(app)

def test_create_worklog_success():
    fake_user = MagicMock(spec=User)
    fake_user.id = 1
    
    fake_board = MagicMock(spec=Board)
    fake_board.id = 1
    fake_board.user_id = 1
    
    fake_card = MagicMock(spec=Card)
    fake_card.id = 10
    fake_card.board_id = 1
    
    mock_db = MagicMock()
    # Mock check_card_access logic
    mock_db.query.return_value.filter.return_value.first.side_effect = [fake_card, fake_board]
    
    def mock_refresh(obj):
        obj.id = 1
    mock_db.refresh.side_effect = mock_refresh
    
    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    payload = {
        "date": str(date.today()),
        "hours": 2.5,
        "note": "Test worklog"
    }
    
    response = client.post("/cards/10/worklogs", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["hours"] == 2.5
    assert data["note"] == "Test worklog"
    assert mock_db.add.called
    assert mock_db.commit.called
    
    app.dependency_overrides.clear()

def test_get_card_worklogs():
    fake_user = MagicMock(spec=User)
    fake_user.id = 1
    
    fake_card = MagicMock(spec=Card)
    fake_card.id = 10
    fake_card.board_id = 1
    
    fake_board = MagicMock(spec=Board)
    fake_board.id = 1
    fake_board.user_id = 1
    
    now = datetime.now(timezone.utc)
    fake_worklogs = [
        TimeEntry(id=1, user_id=1, card_id=10, date=date.today(), hours=1.0, note="W1", created_at=now, updated_at=now),
        TimeEntry(id=2, user_id=1, card_id=10, date=date.today(), hours=2.0, note="W2", created_at=now, updated_at=now)
    ]
    
    mock_db = MagicMock()
    # First two calls for check_card_access, third for .all()
    mock_db.query.return_value.filter.return_value.first.side_effect = [fake_card, fake_board]
    mock_db.query.return_value.filter.return_value.all.return_value = fake_worklogs
    
    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/cards/10/worklogs")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["note"] == "W1"
    
    app.dependency_overrides.clear()

def test_update_worklog_success():
    fake_user = MagicMock(spec=User)
    fake_user.id = 1
    
    now = datetime.now(timezone.utc)
    fake_worklog = TimeEntry(id=1, user_id=1, card_id=10, date=date.today(), hours=1.0, note="Old", created_at=now, updated_at=now)
    
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_worklog
    
    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    payload = {"hours": 3.0, "note": "Updated"}
    response = client.patch("/worklogs/1", json=payload)
    
    assert response.status_code == 200
    assert fake_worklog.hours == 3.0
    assert fake_worklog.note == "Updated"
    assert mock_db.commit.called
    
    app.dependency_overrides.clear()

def test_delete_worklog_success():
    fake_user = MagicMock(spec=User)
    fake_user.id = 1
    
    fake_worklog = MagicMock(spec=TimeEntry)
    fake_worklog.id = 1
    fake_worklog.user_id = 1
    
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_worklog
    
    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.delete("/worklogs/1")
    
    assert response.status_code == 204
    assert mock_db.delete.called
    assert mock_db.commit.called
    
    app.dependency_overrides.clear()

def test_get_my_worklogs_week():
    fake_user = MagicMock(spec=User)
    fake_user.id = 1
    
    now = datetime.now(timezone.utc)
    # Today is Dec 24, 2025 (Wednesday, Week 52)
    fake_worklogs = [
        TimeEntry(id=1, user_id=1, card_id=10, date=date(2025, 12, 24), hours=4.0, note="Week 52", created_at=now, updated_at=now)
    ]
    
    mock_db = MagicMock()
    # Mock the query chain: query().filter().filter().all()
    mock_db.query.return_value.filter.return_value.filter.return_value.all.return_value = fake_worklogs
    
    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/users/me/worklogs?week=2025-52")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["hours"] == 4.0
    
    app.dependency_overrides.clear()
