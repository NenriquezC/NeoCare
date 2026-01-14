import pytest
from datetime import date
from fastapi import HTTPException
from app.report.services import get_week_date_range

def test_get_week_date_range_valid():
    """✓ Validar conversión de semana ISO a rango de fechas"""
    # Semana 1 de 2026: 2025-12-29 al 2026-01-04
    start, end = get_week_date_range("2026-W01")
    assert start == date(2025, 12, 29)
    assert end == date(2026, 1, 4)

    # Semana 5 de 2025: 2025-01-27 al 2025-02-02
    start, end = get_week_date_range("2025-W05")
    assert start == date(2025, 1, 27)
    assert end == date(2025, 2, 2)

def test_get_week_date_range_invalid_format():
    """✓ Rechazar formato de semana inválido"""
    with pytest.raises(HTTPException) as exc:
        get_week_date_range("2025/05")  # Formato inválido con /
    assert exc.value.status_code == 400
    assert "Formato de semana inválido" in exc.value.detail

    with pytest.raises(HTTPException) as exc:
        get_week_date_range("invalid")  # Texto inválido
    assert exc.value.status_code == 400
    assert "Formato de semana inválido" in exc.value.detail

def test_get_week_date_range_invalid_week():
    """✓ Rechazar semana inexistente (W54)"""
    with pytest.raises(HTTPException) as exc:
        get_week_date_range("2025-W54")
    assert exc.value.status_code == 400
    assert "Semana ISO inválida" in exc.value.detail
