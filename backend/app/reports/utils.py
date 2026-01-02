from datetime import datetime, timedelta

def get_week_range(week_str: str):
    """
    Calcula el inicio (lunes) y fin (domingo) de una semana en formato YYYY-Www.
    Ejemplo: 2026-W01 -> (2025-12-29, 2026-01-04)
    """
    try:
        # El formato %G-W%V-1 indica: Año ISO, Semana ISO, Día 1 (Lunes)
        start_date = datetime.strptime(f"{week_str}-1", "%G-W%V-%u").date()
        end_date = start_date + timedelta(days=6)
        return start_date, end_date
    except ValueError:
        raise ValueError("Formato de semana inválido. Use YYYY-Www (ej: 2026-W01)")
