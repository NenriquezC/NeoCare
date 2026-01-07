# Script para iniciar frontend y backend simultáneamente
$ErrorActionPreference = "Stop"

Write-Host "=== Iniciando NeoCare ===" -ForegroundColor Cyan

# Iniciar backend en una nueva ventana de PowerShell
Write-Host "`n[1/2] Iniciando Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; & ..\\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"

# Esperar un momento
Start-Sleep -Seconds 2

# Iniciar frontend en una nueva ventana de PowerShell
Write-Host "[2/2] Iniciando Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend_t'; npm run dev"

Write-Host "`n✓ Servicios iniciados" -ForegroundColor Cyan
Write-Host "  Backend:  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host "`nPuedes cerrar esta ventana. Los servicios están en ventanas separadas." -ForegroundColor Gray