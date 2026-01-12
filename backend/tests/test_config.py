import pytest
from app.config import Settings, settings

"""
Pruebas para la configuración de la aplicación (app.config.Settings).

Este módulo verifica:
- Los valores por defecto definidos en la instancia `settings`.
- La correcta carga de valores desde variables de entorno al instanciar `Settings`.

Notas:
- `test_valores_por_defecto` comprueba los valores esperados cuando no hay variables
de entorno que los sobrescriban.
- `test_carga_desde_env` utiliza `monkeypatch` para establecer variables de entorno y
validar que `Settings` las lee y convierte a los tipos esperados (p. ej. int).
"""

def test_valores_por_defecto():
    """Comprueba los valores por defecto de la configuración.

    Aserciones:
    - DATABASE_URL está configurada (puede ser SQLite o PostgreSQL según el entorno)
    - SECRET_KEY está definida y no está vacía
    - ALGORITHM y ACCESS_TOKEN_EXPIRE_MINUTES tienen valores correctos
    """
    # En tests, DATABASE_URL puede ser PostgreSQL (configuración base) o SQLite (sobrescrita por TESTING=1)
    # Lo importante es que esté definida
    assert settings.DATABASE_URL is not None
    assert len(settings.DATABASE_URL) > 0
    
    # SECRET_KEY puede venir de .env o usar el default
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 10  # Debe ser una clave razonable
    
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

def test_carga_desde_env(monkeypatch):
    """Verifica que Settings carga y parsea correctamente valores desde variables de entorno.

    Flujo:
    1. Establecer variables de entorno con monkeypatch.
    2. Instanciar Settings y comprobar que los atributos reflejan las variables establecidas.
    Aserciones:
    - DATABASE_URL, SECRET_KEY y ALGORITHM coinciden con las variables de entorno.
    - ACCESS_TOKEN_EXPIRE_MINUTES se convierte correctamente a entero (45).
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./env_test.db")
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    monkeypatch.setenv("ALGORITHM", "HS512")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "45")

    settings_env = Settings()

    assert settings_env.DATABASE_URL == "sqlite:///./env_test.db"
    assert settings_env.SECRET_KEY == "env-secret"
    assert settings_env.ALGORITHM == "HS512"
    assert settings_env.ACCESS_TOKEN_EXPIRE_MINUTES == 45
