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


# ============================
# Semana 6 — Labels (Etiquetas)
# ============================

class LabelCreate(BaseModel):
    """
    Schema para crear una etiqueta (Label) en una tarjeta.
    """
    name: str
    color: str = "blue"


class LabelOut(BaseModel):
    """
    Schema de salida para una etiqueta.
    """
    id: int
    card_id: int
    name: str
    color: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==============================
# Semana 6 — Subtasks (Checklist)
# ==============================

class SubtaskCreate(BaseModel):
    """
    Schema para crear una subtarea (checklist item).
    """
    title: str


class SubtaskUpdate(BaseModel):
    """
    Schema para actualizar una subtarea.
    Permite marcar como completada.
    """
    title: Optional[str] = None
    completed: Optional[bool] = None


class SubtaskOut(BaseModel):
    """
    Schema de salida para una subtarea.
    """
    id: int
    card_id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
