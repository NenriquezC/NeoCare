from pydantic import BaseModel, Field, ConfigDict, field_validator
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

    @field_validator('board_id', 'list_id', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convierte strings a int para compatibilidad con Postman/Newman"""
        if v is None:
            return v
        if isinstance(v, str):
            return int(v)
        return v



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

    @field_validator('list_id', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convierte strings a int para compatibilidad con Postman/Newman"""
        if v is None:
            return v
        if isinstance(v, str):
            return int(v)
        return v


#Codigo de las Semana 3
class CardMove(BaseModel):
    """
    Esquema para mover/reordenar una tarjeta (Semana 3 Drag & Drop).

    Campos:
    - list_id (int): columna destino.
    - order (int): nueva posición dentro de la columna destino (>= 0).
    """
    list_id:int
    order: int = Field(..., ge=0, description="Posición destino (>= 0)")

    @field_validator('list_id', 'order', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convierte strings a int para compatibilidad con Postman/Newman"""
        if v is None:
            return v
        if isinstance(v, str):
            return int(v)
        return v


# =====================================================================================
# 🏷️ SEMANA 6 - SCHEMAS DE LABELS (ETIQUETAS)
# =====================================================================================

class LabelBase(BaseModel):
    """
    Esquema base para Labels/Etiquetas
    
    Las etiquetas permiten categorizar y priorizar tarjetas visualmente
    """
    name: str = Field(..., min_length=1, max_length=50, description="Nombre de la etiqueta (ej: 'Urgente', 'Bug', 'Feature')")
    color: Optional[str] = Field(None, max_length=20, description="Color en formato HEX (#ef4444) o nombre (red)")


class LabelCreate(LabelBase):
    """
    Esquema para crear una nueva etiqueta
    
    Ejemplo de uso Frontend:
    ```json
    {
        "name": "Urgente",
        "color": "#ef4444"
    }
    ```
    
    Colores sugeridos:
    - Rojo (#ef4444): Urgente, Bugs críticos
    - Amarillo (#f59e0b): Prioridad media, Pendiente
    - Verde (#10b981): Completado, Aprobado
    - Azul (#3b82f6): Feature, Info
    - Púrpura (#8b5cf6): QA, Testing
    - Gris (#6b7280): Bloqueado, En espera
    """
    pass


class LabelOut(LabelBase):
    """
    Esquema de salida para etiquetas
    
    Incluye el ID generado por la base de datos y la relación con la tarjeta
    
    Ejemplo de response:
    ```json
    {
        "id": 1,
        "card_id": 123,
        "name": "Urgente",
        "color": "#ef4444"
    }
    ```
    """
    id: int
    card_id: int
    model_config = ConfigDict(from_attributes=True)


# =====================================================================================
# ✅ SEMANA 6 - SCHEMAS DE SUBTASKS (CHECKLIST)
# =====================================================================================

class SubtaskBase(BaseModel):
    """
    Esquema base para Subtasks/Checklist
    
    Las subtasks permiten dividir una tarjeta en tareas más pequeñas
    """
    title: str = Field(..., min_length=1, max_length=200, description="Descripción de la subtarea")
    completed: bool = Field(default=False, description="Indica si la subtarea está completada")


class SubtaskCreate(SubtaskBase):
    """
    Esquema para crear una nueva subtarea
    
    Ejemplo de uso Frontend:
    ```json
    {
        "title": "Escribir documentación de API",
        "completed": false
    }
    ```
    
    El campo 'completed' es opcional y por defecto es False
    """
    pass


class SubtaskUpdate(BaseModel):
    """
    Esquema para actualizar una subtarea existente
    
    Todos los campos son opcionales (PATCH parcial)
    
    Ejemplos de uso Frontend:
    
    1. Marcar como completada:
    ```json
    {
        "completed": true
    }
    ```
    
    2. Cambiar título:
    ```json
    {
        "title": "Nuevo título actualizado"
    }
    ```
    
    3. Reordenar:
    ```json
    {
        "position": 3
    }
    ```
    
    4. Actualizar varios campos:
    ```json
    {
        "title": "Título nuevo",
        "completed": true,
        "position": 1
    }
    ```
    """
    title: Optional[str] = None
    completed: Optional[bool] = None
    position: Optional[int] = None


class SubtaskOut(SubtaskBase):
    """
    Esquema de salida para subtareas
    
    Incluye ID, posición y relación con la tarjeta
    
    Ejemplo de response:
    ```json
    {
        "id": 1,
        "card_id": 123,
        "title": "Implementar endpoint de búsqueda",
        "completed": true,
        "position": 0
    }
    ```
    
    Para calcular progreso en Frontend:
    ```javascript
    const subtasks = [...]; // Array de SubtaskOut
    const completed = subtasks.filter(s => s.completed).length;
    const total = subtasks.length;
    const percentage = Math.round((completed / total) * 100);
    // Ejemplo: "✓ 3/7 completadas (43%)"
    ```
    """
    id: int
    card_id: int
    position: int
    model_config = ConfigDict(from_attributes=True)


# =====================================================================================
# 📋 CARD OUT - SCHEMA DE SALIDA COMPLETO
# =====================================================================================

class CardOut(BaseModel):
    """
    Esquema de salida (read/model) que representa una tarjeta tal como se devuelve desde la API.
    
    🆕 SEMANA 6: Ahora incluye labels y subtasks

    Campos:
    - id (int): Identificador único de la tarjeta.
    - board_id (int): Identificador del tablero al que pertenece la tarjeta.
    - list_id (int): Identificador de la lista contenedora.
    - order (int): Posición de la tarjeta dentro de la lista (Semana 3)
    - title (str): Título de la tarjeta.
    - description (Optional[str]): Descripción de la tarjeta.
    - due_date (Optional[date]): Fecha límite (solo fecha).
    - created_by_id (int): Identificador del usuario que creó la tarjeta.
    - responsible_id (Optional[int]): Identificador del usuario responsable de la tarjeta (si aplica).      
    - created_at (datetime): Marca temporal de creación.
    - updated_at (datetime): Marca temporal de la última actualización.
    - archived (bool): Indica si la tarjeta está archivada.
    - labels (list[LabelOut]): Etiquetas asociadas (Semana 6)
    - subtasks (list[SubtaskOut]): Checklist de subtareas (Semana 6)

    Configuración:
    - from_attributes = True para permitir compatibilidad con objetos ORM (p. ej., SQLAlchemy).
    
    Ejemplo de response completo:
    ```json
    {
        "id": 123,
        "board_id": 1,
        "list_id": 2,
        "order": 0,
        "title": "Implementar búsqueda global",
        "description": "Añadir endpoint y UI",
        "due_date": "2026-01-15",
        "created_by_id": 1,
        "responsible_id": 5,
        "created_at": "2026-01-07T10:00:00Z",
        "updated_at": "2026-01-07T12:00:00Z",
        "archived": false,
        "labels": [
            {"id": 1, "card_id": 123, "name": "Feature", "color": "#3b82f6"},
            {"id": 2, "card_id": 123, "name": "Urgente", "color": "#ef4444"}
        ],
        "subtasks": [
            {"id": 1, "card_id": 123, "title": "Crear endpoint", "completed": true, "position": 0},
            {"id": 2, "card_id": 123, "title": "Implementar UI", "completed": false, "position": 1}
        ]
    }
    ```
    """
    id: int
    board_id: int
    list_id: int
    order: int  # Semana 3
    title: str
    description: Optional[str]
    due_date: Optional[date]
    created_by_id: int
    responsible_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    archived: bool
    labels: list[LabelOut] = []  # Semana 6
    subtasks: list[SubtaskOut] = []  # Semana 6

    model_config = ConfigDict(from_attributes=True)

