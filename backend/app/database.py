from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# =============================
# 1) URL DE CONEXIÓN A POSTGRES
# =============================
# Cambia TU_PASSWORD y el nombre de la base
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Limon1307@localhost:5432/neocare"
)

# =============================
# 2) CREAR ENGINE
# =============================
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=True  # muestra SQL en consola (útil en desarrollo)
)

# =============================
# 3) SESIONES
# =============================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =============================
# 4) BASE PARA LOS MODELOS
# =============================
Base = declarative_base()