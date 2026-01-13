"""
Servicios del módulo Report — Semana 5.

Este archivo contiene la lógica de negocio reutilizable para la generación
del Informe Semanal. Aquí NO se definen rutas HTTP ni esquemas de respuesta,
solo funciones puras y helpers que serán usados por los endpoints.

Responsabilidades principales:
- Convertir una semana ISO (YYYY-WW) en un rango de fechas real (lunes a domingo).
- Validar que un usuario tenga acceso a un tablero (owner o miembro).

Notas de diseño:
- No depende del frontend.
- Minimiza lógica en routes.py.
- Facilita testing unitario y reutilización.
"""

from datetime import date
import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..boards.models import Board, BoardMember


def get_week_date_range(week: str) -> tuple[date, date]:
    """
    Convierte una semana en formato ISO 'YYYY-WW' en un rango de fechas reales.

    La semana ISO comienza siempre en lunes (día 1) y termina en domingo (día 7).
    Este rango será utilizado para filtrar tarjetas y registros de tiempo
    en todos los endpoints del informe semanal.

    Args:
        week (str): Semana en formato ISO, por ejemplo '2025-W05'.

    Returns:
        tuple[date, date]:
            - start_date (date): lunes de la semana indicada.
            - end_date (date): domingo de la semana indicada.

    Raises:
        HTTPException (400):
            - Si el formato de la semana no es válido.
            - Si la semana no existe en el calendario ISO.

    Ejemplo:
        >>> get_week_date_range("2025-W05")
        (date(2025, 1, 27), date(2025, 2, 2))

    Importancia:
        Esta función es transversal:
        - summary
        - hours-by-user
        - hours-by-card

        Si esta lógica falla, TODO el informe falla.
    """
    # Validación de formato ISO básico: YYYY-WW
    if not re.match(r"^\d{4}-W\d{2}$", week):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de semana inválido. Usa 'AAAA-WW'."
        )

    try:
        year_str, week_str = week.split("-W")
        year = int(year_str)
        week_number = int(week_str)

        # ISO calendar:
        # - lunes = 1
        # - domingo = 7
        start_date = date.fromisocalendar(year, week_number, 1)
        end_date = date.fromisocalendar(year, week_number, 7)

    except ValueError:
        # Captura semanas inexistentes (ej: W54)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Semana ISO inválida."
        )

    return start_date, end_date


def verify_board_access(db: Session, board_id: int, user_id: int) -> None:
    """
    Verifica que un usuario tenga acceso a un tablero específico.

    Un usuario tiene acceso si:
    - Es el propietario del tablero (boards.user_id)
    - O es miembro del tablero (board_members)

    Esta validación es obligatoria para TODOS los endpoints del módulo report
    y cumple con los requisitos de seguridad de la Semana 5.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        board_id (int): ID del tablero a consultar.
        user_id (int): ID del usuario autenticado.

    Returns:
        None

    Raises:
        HTTPException (404):
            - Si el tablero no existe.
        HTTPException (403):
            - Si el usuario no tiene permisos sobre el tablero.

    Diseño:
        - Centraliza la lógica de permisos.
        - Evita duplicar validaciones en cada endpoint.
        - Facilita cambios futuros en reglas de acceso.
    """
    board = db.query(Board).filter(Board.id == board_id).first()

    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tablero no encontrado."
        )

    # Caso 1: el usuario es el owner del tablero
    if board.user_id == user_id:
        return

    # Caso 2: el usuario es miembro del tablero
    membership = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este tablero."
        )

    return