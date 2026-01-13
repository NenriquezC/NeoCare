"""
Archivo principal de arranque del backend NeoCare.

Inicializa el servidor FastAPI, configura la política CORS para permitir llamadas
desde el frontend, incluye las rutas de autenticación y expone el endpoint raíz
de verificación de estado.
"""
from fastapi import FastAPI  # Importa la clase FastAPI que se usa para crear la aplicación web/servidor.
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import router as auth_router  # importa las rutas de auth
from .boards.routes import router as boards_router
from .cards.routes import router as cards_router  # ✅ agrega cards aquí, arriba, como los demás
from .worklogs.routes import router as worklogs_router  # ✅ Semana 4: worklogs
from app.report.routes import router as report_router
from app.error_utils import http_exception_handler, sqlalchemy_exception_handler, generic_exception_handler
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.logging_config import *
# Inicializa la aplicación FastAPI con título personalizado
app = FastAPI(title="NeoCare API", redirect_slashes=False)

# --- Registro de manejadores globales de errores ---
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# CORS (para que el frontend pueda llamar al backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ¡En producción, define los dominios permitidos!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra las rutas
app.include_router(auth_router)
app.include_router(boards_router)
app.include_router(cards_router)  # ✅ incluye cards aquí también (en orden)
app.include_router(worklogs_router)  # ✅ Semana 4: incluye worklogs
app.include_router(report_router)

@app.get("/")
def root():
    """
    Endpoint raíz (health check).

    Permite verificar si el backend de NeoCare está operativo.
    """
    return {"status": "NeoCare Backend Running"}

@app.get("/debug/database-info")
def database_info():
    """Endpoint temporal para verificar qué base de datos se está usando"""
    from .database import DATABASE_URL, IS_TESTING
    return {
        "database_url": DATABASE_URL,
        "is_testing": IS_TESTING,
        "database_type": "SQLite" if IS_TESTING else "PostgreSQL"
    }
