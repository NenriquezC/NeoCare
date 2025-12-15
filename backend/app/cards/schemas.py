from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

"""
Módulo de modelos Pydantic para operaciones sobre "cards" (tarjetas) en un tablero.

Modelos:
- CardCreate: esquema para la creación de una nueva tarjeta.
- CardUpdate: esquema para actualización parcial de una tarjeta existente.
- CardOut: esquema de salida (representación) de una tarjeta tal como se devuelve desde la API/ORMS.

Notas:
- Se usa pydantic para validación automática de tipos y restricciones.
- Las fechas usan date (para due_date) y datetime (para created_at/updated_at).
"""


class CardCreate(BaseModel):
    """
    Esquema para crear una tarjeta (Card).

    Campos:
    - title (str): Título obligatorio de la tarjeta. Tiene longitud mínima de 1 carácter.
    - description (Optional[str]): Descripción opcional de la tarjeta.
    - due_date (Optional[date]): Fecha límite opcional para la tarjeta (solo fecha).
    - board_id (int): Identificador del tablero al que pertenece la tarjeta.
    - list_id (int): Identificador de la lista dentro del tablero donde se crea la tarjeta.

    Validación destacada:
    - title usa Field(..., min_length=1) para asegurar que no esté vacío.
    """
    title: str = Field(..., min_length=1, description="Título obligatorio")
    description: Optional[str] = None
    due_date: Optional[date] = None
    board_id: int
    list_id: int



class CardUpdate(BaseModel):
    """
    Esquema para actualizar parcialmente una tarjeta existente.

    Campos (todos opcionales):
    - title (Optional[str]): Nuevo título; si se proporciona, debe ser una cadena.
    - description (Optional[str]): Nueva descripción.
    - due_date (Optional[date]): Nueva fecha límite (solo fecha).
    - list_id (Optional[int]): Nuevo identificador de lista para mover la tarjeta.
    - archived (Optional[bool]): Marcar/desmarcar la tarjeta como archivada.

    Uso:
    - Este modelo se usa para PATCH/PUT parcial donde solo se envían los campos a modificar.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    list_id: Optional[int] = None
    archived: Optional[bool] = None



class CardOut(BaseModel):
    """
    Esquema de salida (read/model) que representa una tarjeta tal como se devuelve desde la API.

    Campos:
    - id (int): Identificador único de la tarjeta.
    - board_id (int): Identificador del tablero al que pertenece la tarjeta.
    - list_id (int): Identificador de la lista contenedora.
    - title (str): Título de la tarjeta.
    - description (Optional[str]): Descripción de la tarjeta.
    - due_date (Optional[date]): Fecha límite (solo fecha).
    - created_by_id (int): Identificador del usuario que creó la tarjeta.
    - responsible_id (Optional[int]): Identificador del usuario responsable de la tarjeta (si aplica).
    - created_at (datetime): Marca temporal de creación.
    - updated_at (datetime): Marca temporal de la última actualización.
    - archived (bool): Indica si la tarjeta está archivada.

    Configuración:
    - orm_mode = True para permitir compatibilidad con objetos ORM (p. ej., SQLAlchemy).
    """
    id: int
    board_id: int
    list_id: int
    title: str
    description: Optional[str]
    due_date: Optional[date]
    created_by_id: int
    responsible_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    archived: bool

    class Config:
        orm_mode = True