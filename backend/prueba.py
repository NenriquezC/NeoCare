"""
Módulo FastAPI de ejemplo simple.

Expone dos endpoints:
- "/"        : Mensaje de bienvenida y verificación de estado.
- "/items/{item_id}" : Retorna información de un ítem usando parámetros de path y query.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
Módulo FastAPI de ejemplo simple.

Expone dos endpoints:
- "/"        : Mensaje de bienvenida y verificación de estado.
- "/items/{item_id}" : Retorna información de un ítem usando parámetros de path y query.
"""
    return {"message": "Hola Néstor, FastAPI ya está funcionando 🚀"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """
    Obtiene la información de un ítem según su ID y parámetro opcional de búsqueda.

    Args:
        item_id (int): Identificador del ítem recibido desde la URL (path).
        q (str, optional): Parámetro de consulta (query string) opcional.

    Returns:
        dict: Diccionario con el ID del ítem, query recibido y mensaje de prueba.
    """
    return {
        "item_id": item_id,
        "q": q,
        "mensaje": "Este es tu primer endpoint con path + query params",
    }