
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#URL de conexión a PostgreSQL
# 
SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/neocare_db"
)

#Crea el engine (conexión física a la BD)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,      
    future=True,    
)

#Crea la fábrica de sesiones (cada request usará una sesión)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

#Base para declarar  modelos (User, Board, etc.)
Base = declarative_base()


#Dependency para FastAPI: la usarás en las rutas con Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()