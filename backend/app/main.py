# app/main.py
#Es la base del backend.
#Crea el servidor que recibirá peticiones del frontend, devolverá datos, validará JWT, conectará a PostgreSQL
#manejará toda la lógica del proyecto NeoCare.
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import router as auth_router  #importa las rutas de auth
from .boards.routes import router as boards_router 

app = FastAPI(title="NeoCare API")

# CORS (para que el frontend pueda llamar al backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego lo ajustas si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 REGISTRAR RUTAS DE AUTH
app.include_router(auth_router)
app.include_router(boards_router) 

@app.get("/")
def root():
    return {"status": "NeoCare Backend Running"}