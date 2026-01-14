from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger("neocare.errors")

# Estructura de error uniforme

def error_response(status_code: int, detail: str, extra: dict = None):
    payload = {"detail": detail}
    if extra:
        payload.update(extra)
    return JSONResponse(status_code=status_code, content=payload)

# Handler para HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail}")
    return error_response(exc.status_code, exc.detail)

# Handler para errores de SQLAlchemy
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"SQLAlchemyError: {str(exc)}")
    return error_response(500, "Error interno de base de datos")

# Handler para errores no controlados
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return error_response(500, "Error interno del servidor")
