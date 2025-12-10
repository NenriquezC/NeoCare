"""
Archivo principal de arranque del backend NeoCare.

Inicializa el servidor FastAPI, configura la política CORS para permitir llamadas
desde el frontend, incluye las rutas de autenticación y expone el endpoint raíz
de verificación de estado.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import router as auth_router  #importa las rutas de auth
from .boards.routes import router as boards_router 

# Inicializa la aplicación FastAPI con título personalizado
app = FastAPI(title="NeoCare API")

# CORS (para que el frontend pueda llamar al backend)
app.add_middleware(


    CORSMiddleware,
    allow_origins=["*"],   #¡En producción, define los dominios permitidos!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra las rutas de autenticación bajo el router correspondiente
app.include_router(auth_router)
app.include_router(boards_router) 

@app.get("/")
def root():
    """
    Endpoint raíz (health check).

    Permite verificar si el backend de NeoCare está operativo.
    """
    return {"status": "NeoCare Backend Running"}