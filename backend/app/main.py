"""
Archivo principal de arranque del backend NeoCare.

Inicializa el servidor FastAPI, configura la política CORS para permitir llamadas
desde el frontend, incluye las rutas de autenticación y expone el endpoint raíz
de verificación de estado.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .auth.routes import router as auth_router
from .boards.routes import router as boards_router
from .cards.routes import router as cards_router
from .worklogs.routes import router as worklogs_router
from app.report.routes import router as report_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa la aplicación FastAPI con título personalizado
app = FastAPI(
    title="NeoCare API",
    description="API para gestión de proyectos Kanban con registro de horas",
    version="1.0.0"
)

# Middleware para logging de requests (solo en desarrollo)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Solo log en desarrollo, sin emojis para evitar problemas de encoding
        if process_time > 1.0:  # Solo loggear requests lentos
            print(f"SLOW REQUEST: {request.method} {request.url.path} - {process_time:.2f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        print(f"ERROR: {request.method} {request.url.path} - {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )

# CORS (para que el frontend pueda llamar al backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://neocare-frontend.vercel.app"  # Actualizar con tu URL de Vercel
    ],
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
