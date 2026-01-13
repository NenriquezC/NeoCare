"""
Script manual para probar el módulo de reportes
"""
import sys
sys.path.insert(0, '.')

from app.report.services import get_week_date_range

# Test 1: Validar cálculo de semana ISO
print("=" * 60)
print("TEST 1: Validación de semanas ISO")
print("=" * 60)

test_weeks = [
    "2026-W01",  # Primera semana de 2026
    "2026-W02",  # Segunda semana
    "2025-W52",  # Última semana de 2025
]

for week in test_weeks:
    try:
        start, end = get_week_date_range(week)
        print(f"✅ {week}: {start} (lun) → {end} (dom)")
    except Exception as e:
        print(f"❌ {week}: Error - {e}")

# Test 2: Validar semanas inválidas
print("\n" + "=" * 60)
print("TEST 2: Validación de semanas inválidas")
print("=" * 60)

invalid_weeks = [
    "2026-W54",  # Semana 54 no existe
    "2026-W00",  # Semana 0 no existe
    "2026W01",   # Formato incorrecto (sin guión)
    "W01-2026",  # Formato invertido
]

for week in invalid_weeks:
    try:
        start, end = get_week_date_range(week)
        print(f"❌ {week}: Debería fallar pero pasó - {start} → {end}")
    except Exception as e:
        print(f"✅ {week}: Rechazado correctamente - {type(e).__name__}")

print("\n" + "=" * 60)
print("TESTS COMPLETADOS")
print("=" * 60)

