"""Tests simplificados de integración para reportes"""
import pytest
from datetime import date, datetime

from app.boards.models import User, Board, List, Card, TimeEntry
from app.auth.utils import create_token, hash_password


def test_report_simple(client):
    """Test simple para verificar que los reportes funcionan con datos básicos"""
    # Registrar usuario
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "reporttest@example.com",
        "password": "password123"
    })
    assert response.status_code == 200

    # Login
    response = client.post("/auth/login", json={
        "email": "reporttest@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Obtener tableros (se crea uno automáticamente)
    response = client.get("/boards/", headers=headers)
    assert response.status_code == 200
    boards = response.json()
    assert len(boards) == 1
    board_id = boards[0]["id"]

    # Verificar resumen (vacío por ahora)
    response = client.get(f"/report/{board_id}/summary?week=2026-01", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"]["count"] == 0
    assert data["new"]["count"] == 0
    assert data["overdue"]["count"] == 0

