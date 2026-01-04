"""
Schemas Pydantic del módulo Report — Semana 5.

Este archivo define los modelos de respuesta utilizados por los endpoints
del informe semanal. Estos schemas representan el contrato oficial entre
el backend y el frontend.

Responsabilidades:
- Definir estructuras de salida claras y tipadas.
- Facilitar validación automática de respuestas.
- Mejorar la documentación generada por Swagger / OpenAPI.

Notas:
- Estos schemas NO contienen lógica.
- Se utilizan únicamente para serializar datos hacia el frontend.
"""

from pydantic import BaseModel
from typing import List, Optional


class CardSummaryItem(BaseModel):
    """
    Representa una tarjeta en los listados del resumen semanal.

    Se utiliza tanto para tareas completadas, nuevas y vencidas.
    """
    id: int
    title: str
    responsible_id: Optional[int] = None


class SummaryBlock(BaseModel):
    """
    Bloque genérico del resumen semanal.

    Contiene:
    - el total de elementos
    - una lista reducida de tarjetas asociadas
    """
    count: int
    items: List[CardSummaryItem]


class WeeklySummaryResponse(BaseModel):
    """
    Respuesta completa del endpoint /report/{board_id}/summary.

    Agrupa los tres bloques principales del informe semanal:
    - completadas
    - nuevas
    - vencidas
    """
    completed: SummaryBlock
    new: SummaryBlock
    overdue: SummaryBlock