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
    - DATABASE_URL tiene la ruta de prueba por defecto.
    - SECRET_KEY, ALGORITHM y ACCESS_TOKEN_EXPIRE_MINUTES coinciden con los valores esperados.
    """
    assert settings.DATABASE_URL == "sqlite:///./test.db"
    assert settings.SECRET_KEY == "your-secret-key-here"
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
