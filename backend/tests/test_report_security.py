"""
Tests de Seguridad del Módulo Report — Semana 5

Valida que las protecciones de autenticación y autorización
funcionan correctamente en todos los endpoints del informe semanal.

Prioridad: CRÍTICA
- Evitar acceso no autorizado a datos sensibles.
- Garantizar que solo usuarios con permisos vean informes de sus tableros.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime, timezone
from decimal import Decimal

from tests.conftest import TestingSessionLocal
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember
from app.main import app

client = TestClient(app)


def crear_usuario_y_token(client, email_suffix=""):
    """Helper: crea usuario y obtiene token JWT"""
    email = f"test_{email_suffix}@example.com"
    payload = {
        "email": email,
        "password": "password123",
        "name": f"User {email_suffix}",
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    token = data["access_token"]

    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user, token


def crear_tablero_completo(user_id: int):
    """Helper: crea tablero con lista y tarjeta con horas"""
    db = TestingSessionLocal()

    # Tablero
    board = Board(name="Security Test Board", user_id=user_id)
    db.add(board)
    db.commit()
    db.refresh(board)

    # Lista "Hecho"
    done_list = List(name="Hecho", board_id=board.id, position=0)
    db.add(done_list)
    db.commit()
    db.refresh(done_list)

    # Tarjeta
    card = Card(
        title="Test Card",
        board_id=board.id,
        list_id=done_list.id,
        created_by_id=user_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    # Registro de horas
    worklog = TimeEntry(
        user_id=user_id,
        card_id=card.id,
        date=date.today(),
        hours=Decimal("5.0"),
        note="Testing security"
    )
    db.add(worklog)
    db.commit()

    board_id = board.id
    db.close()
    return board_id


# =============================================================================
# SEGURIDAD: ENDPOINTS SIN TOKEN
# =============================================================================

def test_summary_without_token():
    """Seguridad: GET /report/{board_id}/summary sin token debe retornar 401"""
    resp = client.get("/report/1/summary?week=2026-01")
    assert resp.status_code in [401, 403], f"Expected 401 or 403, got {resp.status_code}"


def test_hours_by_user_without_token():
    """Seguridad: GET /report/{board_id}/hours-by-user sin token debe retornar 401"""
    resp = client.get("/report/1/hours-by-user?week=2026-01")
    assert resp.status_code in [401, 403], f"Expected 401 or 403, got {resp.status_code}"


def test_hours_by_card_without_token():
    """Seguridad: GET /report/{board_id}/hours-by-card sin token debe retornar 401"""
    resp = client.get("/report/1/hours-by-card?week=2026-01")
    assert resp.status_code in [401, 403], f"Expected 401 or 403, got {resp.status_code}"


# =============================================================================
# SEGURIDAD: ACCESO A TABLERO AJENO
# =============================================================================

def test_summary_tablero_ajeno_owner_vs_noowner():
    """Seguridad: No permitir ver summary de tablero ajeno (usuario no es owner ni miembro)"""
    import uuid

    # Usuario 1: owner del tablero
    user1, token1 = crear_usuario_y_token(client, f"owner_{uuid.uuid4().hex[:8]}")
    board_id = crear_tablero_completo(user1.id)

    # Usuario 2: NO relacionado con el tablero
    user2, token2 = crear_usuario_y_token(client, f"stranger_{uuid.uuid4().hex[:8]}")

    # Usuario 1 puede ver su propio tablero
    resp1 = client.get(f"/report/{board_id}/summary?week=2026-01", headers={"Authorization": f"Bearer {token1}"})
    assert resp1.status_code == 200, f"Owner should access, got {resp1.status_code}"

    # Usuario 2 NO puede ver tablero ajeno
    resp2 = client.get(f"/report/{board_id}/summary?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp2.status_code == 403, f"Stranger should get 403, got {resp2.status_code}"
    assert "acceso" in resp2.json()["detail"].lower()


def test_hours_by_user_tablero_ajeno():
    """Seguridad: No permitir ver hours-by-user de tablero ajeno"""
    import uuid

    user1, token1 = crear_usuario_y_token(client, f"owner_{uuid.uuid4().hex[:8]}")
    board_id = crear_tablero_completo(user1.id)

    user2, token2 = crear_usuario_y_token(client, f"stranger_{uuid.uuid4().hex[:8]}")

    resp = client.get(f"/report/{board_id}/hours-by-user?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 403
    assert "acceso" in resp.json()["detail"].lower()


def test_hours_by_card_tablero_ajeno():
    """Seguridad: No permitir ver hours-by-card de tablero ajeno"""
    import uuid

    user1, token1 = crear_usuario_y_token(client, f"owner_{uuid.uuid4().hex[:8]}")
    board_id = crear_tablero_completo(user1.id)

    user2, token2 = crear_usuario_y_token(client, f"stranger_{uuid.uuid4().hex[:8]}")

    resp = client.get(f"/report/{board_id}/hours-by-card?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 403
    assert "acceso" in resp.json()["detail"].lower()


# =============================================================================
# SEGURIDAD: MIEMBROS DEL TABLERO SÍ TIENEN ACCESO
# =============================================================================

def test_member_can_access_summary():
    """Seguridad: Un miembro (no owner) SÍ puede ver el informe del tablero"""
    import uuid

    # Usuario 1: owner
    user1, token1 = crear_usuario_y_token(client, f"owner_{uuid.uuid4().hex[:8]}")
    board_id = crear_tablero_completo(user1.id)

    # Usuario 2: miembro
    user2, token2 = crear_usuario_y_token(client, f"member_{uuid.uuid4().hex[:8]}")

    # Agregar usuario 2 como miembro
    db = TestingSessionLocal()
    member = BoardMember(board_id=board_id, user_id=user2.id, role="member")
    db.add(member)
    db.commit()
    db.close()

    # Usuario 2 (miembro) debe poder acceder
    resp = client.get(f"/report/{board_id}/summary?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 200, f"Member should access, got {resp.status_code}"


def test_member_can_access_hours():
    """Seguridad: Un miembro puede ver hours-by-user y hours-by-card"""
    import uuid

    user1, token1 = crear_usuario_y_token(client, f"owner_{uuid.uuid4().hex[:8]}")
    board_id = crear_tablero_completo(user1.id)

    user2, token2 = crear_usuario_y_token(client, f"member_{uuid.uuid4().hex[:8]}")

    db = TestingSessionLocal()
    member = BoardMember(board_id=board_id, user_id=user2.id, role="member")
    db.add(member)
    db.commit()
    db.close()

    # hours-by-user
    resp1 = client.get(f"/report/{board_id}/hours-by-user?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp1.status_code == 200

    # hours-by-card
    resp2 = client.get(f"/report/{board_id}/hours-by-card?week=2026-01", headers={"Authorization": f"Bearer {token2}"})
    assert resp2.status_code == 200


# =============================================================================
# SEGURIDAD: TABLERO INEXISTENTE
# =============================================================================

def test_summary_tablero_inexistente():
    """Seguridad: Tablero inexistente debe retornar 404"""
    import uuid

    user, token = crear_usuario_y_token(client, f"user_{uuid.uuid4().hex[:8]}")

    resp = client.get("/report/999999/summary?week=2026-01", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404
    assert "no encontrado" in resp.json()["detail"].lower()

