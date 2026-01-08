"""
Schemas (Pydantic) para Worklogs (Semana 4).

Nota importante:
- En base de datos usamos el modelo TimeEntry (tabla time_entries) que YA existe.
- Estos schemas definen el contrato de entrada/salida para la API de horas.
"""

from datetime import date as date_type, datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


# ---------------------------
# SALIDA (API -> Frontend)
# ---------------------------
class WorklogOut(BaseModel):
    """
    Worklog (TimeEntry) que se devuelve al frontend.
    """
    id: int
    user_id: int
    card_id: int
    date: date_type
    hours: Decimal
    note: Optional[str] = None

    # Semana 4: timestamps requeridos
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# ENTRADA: CREAR
# ---------------------------
class WorklogCreate(BaseModel):
    """
    Datos para crear un registro de horas.

    Reglas Semana 4:
    - hours > 0
    - note <= 200
    """
    card_id: int  # Semana 4: asociación obligatoria a tarjeta
    date: date_type
    hours: Annotated[
        Decimal,
        Field(gt=0, max_digits=5, decimal_places=2, description="Horas trabajadas (> 0)")
    ]
    note: Annotated[
        Optional[str],
        Field(default=None, max_length=200, description="Nota opcional (<= 200)")
    ]

    @field_validator('card_id', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convierte strings a int para compatibilidad con Postman/Newman"""
        if v is None:
            return v
        if isinstance(v, str):
            return int(v)
        return v


# ---------------------------
# ENTRADA: EDITAR
# ---------------------------
class WorklogUpdate(BaseModel):
    """
    Datos para editar un worklog.
    Permite actualizar uno o más campos.
    """
    date: Optional[date_type] = None
    hours: Annotated[
        Optional[Decimal],
        Field(None, gt=0, max_digits=5, decimal_places=2)
    ] = None
    note: Annotated[
        Optional[str],
        Field(None, max_length=200)
    ] = None


# ---------------------------
# RESPUESTA: MIS HORAS (SEMANA)
# ---------------------------
class MyHoursDayTotal(BaseModel):
    """
    Totales por día para la vista "Mis horas".
    """
    date: date_type
    total_hours: Decimal


class MyHoursWeekSummary(BaseModel):
    """
    Resumen semanal para la vista "Mis horas".
    """
    week: str  # ejemplo: "2025-W52"
    total_hours: Decimal
    by_day: list[MyHoursDayTotal]
    entries: list[WorklogOut]