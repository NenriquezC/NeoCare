from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración central de la aplicación.

    Esta clase gestiona los principales parámetros de configuración accesibles
    mediante variables de entorno (o valores por defecto). Utiliza Pydantic para
    permitir validaciones automáticas y organización estructurada.

    Atributos:
        DATABASE_URL (str): Cadena de conexión para la base de datos.
        SECRET_KEY (str): Clave secreta para la generación y validación de JWT.
        ALGORITHM (str): Algoritmo utilizado para firmar los tokens JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tiempo de expiración (minutos) para los tokens de acceso.
    """
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        """
        Configuración adicional para Pydantic Settings.

        Especifica el archivo '.env' como fuente de los valores de entorno.
        """
        env_file = ".env"


settings = Settings()
