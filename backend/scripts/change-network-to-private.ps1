# Script para cambiar el perfil de red de Publico a Privado
# EJECUTAR COMO ADMINISTRADOR

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Cambiando perfil de red de Publico a Privado" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener perfil de red actual
$profile = Get-NetConnectionProfile | Where-Object { $_.InterfaceAlias -eq "Wi-Fi" }

if ($profile) {
    Write-Host "Red actual: $($profile.Name)" -ForegroundColor Yellow
    Write-Host "Categoria actual: $($profile.NetworkCategory)" -ForegroundColor Yellow
    Write-Host ""
    
    if ($profile.NetworkCategory -eq "Public") {
        Write-Host "Cambiando categoria de Public a Private..." -ForegroundColor Green
        try {
            Set-NetConnectionProfile -InterfaceAlias "Wi-Fi" -NetworkCategory Private
            Write-Host ""
            Write-Host "OK - Red cambiada a Privada" -ForegroundColor Green
            Write-Host ""
            Write-Host "Ahora la app movil deberia poder conectarse al backend." -ForegroundColor Green
        } catch {
            Write-Host ""
            Write-Host "ERROR: $_" -ForegroundColor Red
            Write-Host ""
            Write-Host "Intenta ejecutar este script como ADMINISTRADOR" -ForegroundColor Yellow
        }
    } else {
        Write-Host "La red ya esta configurada como Privada. No se necesita cambiar." -ForegroundColor Green
    }
} else {
    Write-Host "No se encontro la interfaz Wi-Fi" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
