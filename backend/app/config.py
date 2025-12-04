from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    #Nombre del proyecto (opcional ptero util para logs, titulos, etc)
    PROJECT_NAME: str = "NeoCareHeath" 

    # --- JWT / Seguridad ---
    # Clave secreta para firmar los tokens JWT.
    # En serio: en producción esto debe venir de una variable de entorno.
    SECRET_KEY: str = "changeme-super-secret-key"

    # Algoritmo que usará python-jose para firmar/verificar JWT
    ALGORITHM: str = "HS256"

    # Tiempo de vida del token de acceso (en minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hora

    # --- Base de datos ---
    # URL de conexión para SQLAlchemy
    # Formato típico:
    # postgresql+psycopg2://usuario:password@host:puerto/nombre_bd
    DATABASE_URL: str = (
        "postgresql+psycopg2://user:password@localhost:5432/neocare_db"
    )

    class Config:
        # Esto le dice a Pydantic que, si existe un archivo .env,
        # puede leer variables desde ahí.
        env_file = ".env"
        env_file_encoding = "utf-8"