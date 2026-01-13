# Utilidades para lanzar errores personalizados y consistentes
from fastapi import HTTPException

def not_found(detail: str = "Recurso no encontrado"):
    raise HTTPException(status_code=404, detail=detail)

def forbidden(detail: str = "No tienes permiso para esta acción"):
    raise HTTPException(status_code=403, detail=detail)

def bad_request(detail: str = "Solicitud inválida"):
    raise HTTPException(status_code=400, detail=detail)

def conflict(detail: str = "Conflicto de datos"):
    raise HTTPException(status_code=409, detail=detail)

def unauthorized(detail: str = "No autenticado"):
    raise HTTPException(status_code=401, detail=detail)
