# Script para iniciar el backend con el entorno virtual correcto
$ErrorActionPreference = "Stop"

# Activar entorno virtual
& ..\\.venv\Scripts\Activate.ps1

# Verificar que estamos usando el Python correcto
Write-Host "Usando Python:" -ForegroundColor Green
python --version
Write-Host "Path:" -ForegroundColor Green
python -c "import sys; print(sys.executable)"

# Iniciar uvicorn
Write-Host "`nIniciando servidor backend..." -ForegroundColor Cyan
uvicorn app.main:app --reload
