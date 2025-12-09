import pytest
from app.config import Settings, settings

def test_valores_por_defecto():
    assert settings.DATABASE_URL == "sqlite:///./test.db"
    assert settings.SECRET_KEY == "your-secret-key-here"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

def test_carga_desde_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./env_test.db")
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    monkeypatch.setenv("ALGORITHM", "HS512")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "45")

    settings_env = Settings()

    assert settings_env.DATABASE_URL == "sqlite:///./env_test.db"
    assert settings_env.SECRET_KEY == "env-secret"
    assert settings_env.ALGORITHM == "HS512"
    assert settings_env.ACCESS_TOKEN_EXPIRE_MINUTES == 45
