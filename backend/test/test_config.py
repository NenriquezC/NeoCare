"""
test_config.py
--------------

Pruebas unitarias para la carga y valores por defecto de la configuración de la
aplicación (app.config.Settings). Estas pruebas asumen que `Settings` es una
clase que lee configuración desde variables de entorno (por ejemplo, usando
pydantic.BaseSettings) y que existe una instancia global `settings` con valores
por defecto.

Cada prueba incluye un docstring que explica su propósito, los pasos realizados
y las consideraciones adicionales para mantener las pruebas robustas y aisladas.
"""
import pytest
from app.config import Settings, settings

def test_valores_por_defecto():
    """
    Verifica los valores por defecto de la configuración.

    Comportamiento esperado:
    - La instancia global `settings` expone los valores por defecto definidos en
    la aplicación cuando no existen variables de entorno que los sobrescriban.
    - Se comprueba que el tipo/valor de `ACCESS_TOKEN_EXPIRE_MINUTES` sea el
    esperado (entero).
    - No se modifica el entorno en esta prueba, por lo que debe ejecutarse en
    un entorno controlado (p. ej. CI o entorno de desarrollo con variables
    por defecto).
    """
    assert settings.DATABASE_URL == "sqlite:///./test.db"
    assert settings.SECRET_KEY == "your-secret-key-here"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

def test_carga_desde_env(monkeypatch):
    """
    Verifica que Settings cargue y convierta correctamente valores desde el entorno.

    Pasos:
    1. Usar `monkeypatch.setenv` para inyectar variables de entorno de prueba.
    2. Instanciar `Settings()` para forzar la lectura desde el entorno actual.
    3. Comprobar que los atributos de la instancia reflejan los valores
    proporcionados por las variables de entorno.

    Consideraciones:
    - `monkeypatch` aísla los cambios en las variables de entorno y los revierte
    al finalizar la prueba, evitando efectos colaterales.
    - `ACCESS_TOKEN_EXPIRE_MINUTES` se inyecta como cadena y se espera que la
    clase `Settings` la convierta a entero; si no es así, la prueba fallará y
    se deberá ajustar la validación en la clase de configuración.
    """
    # EsEstablecer variables de entorno de prueba
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./env_test.db")
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    monkeypatch.setenv("ALGORITHM", "HS512")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "45")

    # Crear nueva instancia para que lea las variables de entorno inyectadas
    settings_env = Settings()

    # Comprobar que los valores han sido leídos y convertidos correctamente
    assert settings_env.DATABASE_URL == "sqlite:///./env_test.db"
    assert settings_env.SECRET_KEY == "env-secret"
    assert settings_env.ALGORITHM == "HS512"
    assert settings_env.ACCESS_TOKEN_EXPIRE_MINUTES == 45