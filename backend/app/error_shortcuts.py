# Utilidades para lanzar errores personalizados y consistentes
from fastapi import HTTPException

def not_found(detail: str = "Recurso no encontrado"):
    raise HTTPException(status_code=404, detail=detail or "Recurso no encontrado")

def forbidden(detail: str = "No tienes permiso para esta acción"):
    raise HTTPException(status_code=403, detail=detail or "No tienes permiso para esta acción")

def bad_request(detail: str = "Solicitud inválida"):
    raise HTTPException(status_code=400, detail=detail or "Solicitud inválida")

def conflict(detail: str = "Conflicto de datos"):
    raise HTTPException(status_code=409, detail=detail or "Conflicto de datos")

def unauthorized(detail: str = "No autenticado"):
    raise HTTPException(status_code=401, detail=detail or "No autenticado")
