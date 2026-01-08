# Script para crear regla de firewall para NeoCare Backend
# Ejecutar como ADMINISTRADOR

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Configurando Firewall para NeoCare Backend" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Ruta al ejecutable de Python del venv
$pythonPath = "C:\Users\usuario\Documents\NeoCare\.venv\Scripts\python.exe"

Write-Host "Creando reglas de firewall..." -ForegroundColor Yellow
Write-Host ""

# Eliminar reglas existentes si las hay
Write-Host "1. Eliminando reglas antiguas (si existen)..." -ForegroundColor Gray
Remove-NetFirewallRule -DisplayName "NeoCare Backend Port 8000" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "NeoCare Backend Python" -ErrorAction SilentlyContinue

# Regla 1: Puerto TCP 8000 (Entrada) - TODOS LOS PERFILES
Write-Host "2. Creando regla para puerto TCP 8000 (todos los perfiles)..." -ForegroundColor Gray
try {
    New-NetFirewallRule -DisplayName "NeoCare Backend Port 8000" `
                        -Direction Inbound `
                        -Action Allow `
                        -Protocol TCP `
                        -LocalPort 8000 `
                        -Profile Any `
                        -Enabled True `
                        -Description "Permite conexiones entrantes al backend NeoCare en puerto 8000 (Public, Private, Domain)"
    Write-Host "   OK - Regla de puerto creada (Public, Private, Domain)" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: $_" -ForegroundColor Red
}

# Regla 2: Aplicacion Python especifica (Entrada) - TODOS LOS PERFILES
Write-Host "3. Creando regla para aplicacion Python (todos los perfiles)..." -ForegroundColor Gray
try {
    New-NetFirewallRule -DisplayName "NeoCare Backend Python" `
                        -Direction Inbound `
                        -Action Allow `
                        -Program $pythonPath `
                        -Profile Any `
                        -Enabled True `
                        -Description "Permite conexiones entrantes a Python del backend NeoCare (Public, Private, Domain)"
    Write-Host "   OK - Regla de aplicacion creada (Public, Private, Domain)" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Configuracion completada" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Reglas creadas:" -ForegroundColor Yellow
Write-Host "  1. Puerto TCP 8000 (entrada) - Public, Private, Domain" -ForegroundColor White
Write-Host "  2. Aplicacion Python (entrada) - Public, Private, Domain" -ForegroundColor White
Write-Host ""
Write-Host "Ahora puedes REACTIVAR el firewall y la app movil deberia funcionar." -ForegroundColor Green
Write-Host ""
Write-Host "Backend accesible en: http://192.168.1.39:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales de prueba:" -ForegroundColor Yellow
Write-Host "  Email: movil@test.com" -ForegroundColor White
Write-Host "  Password: 123456" -ForegroundColor White
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
