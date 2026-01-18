@echo off
echo ========================================
echo Iniciando Tests E2E de NeoCare
echo ========================================
echo.

echo [1/3] Verificando dependencias...
cd backend
python -c "import requests; import pytest" 2>nul
if errorlevel 1 (
    echo ERROR: Faltan dependencias. Instalando...
    pip install requests pytest -q
)

echo [2/3] Verificando si el backend esta corriendo...
python -c "import requests; requests.get('http://127.0.0.1:8000/', timeout=2)" 2>nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo ATENCION: El backend NO esta corriendo
    echo ========================================
    echo.
    echo Por favor, en otra terminal ejecuta:
    echo   cd backend
    echo   uvicorn app.main:app --reload
    echo.
    echo Presiona cualquier tecla cuando el backend este iniciado...
    pause >nul
)

echo [3/3] Ejecutando tests E2E de API...
echo.
python -m pytest tests/e2e/ -v -k "test_api" --tb=short

echo.
echo ========================================
echo Tests E2E completados
echo ========================================
pause

