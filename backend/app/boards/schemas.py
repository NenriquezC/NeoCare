"""
Schemas Pydantic para validación y serialización de datos de tableros y listas.
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ListOut(BaseModel):
    """Schema para serializar una lista (columna de un tablero)."""
    id: int
    name: str
    board_id: int
    position: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardOut(BaseModel):
    """Schema para serializar un tablero."""
    id: int
    name: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
