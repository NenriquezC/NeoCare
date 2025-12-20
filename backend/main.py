from fastapi import FastAPI
from app.database import Base, engine
from app.auth.routes import auth_router
from app.boards.routes import boards_router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend con JWT y Boards")

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}

# Rutas
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(boards_router, prefix="/boards", tags=["Boards"])
