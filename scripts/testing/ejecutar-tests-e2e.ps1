# Script para ejecutar Tests E2E de NeoCare
# Autor: Sistema de Testing NeoCare
# Fecha: 2026-01-14

Write-Host "🧪 NeoCare - Tests End-to-End (E2E)" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto NeoCare" -ForegroundColor Red
    exit 1
}

# Menú de opciones
Write-Host "Selecciona el tipo de tests a ejecutar:" -ForegroundColor Yellow
Write-Host "1. Tests de API (Solo requiere backend)" -ForegroundColor White
Write-Host "2. Tests de UI (Requiere backend + frontend)" -ForegroundColor White
Write-Host "3. Todos los tests E2E" -ForegroundColor White
Write-Host "4. Verificar servicios" -ForegroundColor White
Write-Host "5. Instalar dependencias E2E" -ForegroundColor White
Write-Host "6. Salir`n" -ForegroundColor White

$opcion = Read-Host "Opción"

switch ($opcion) {
    "1" {
        Write-Host "`n📡 Ejecutando Tests de API..." -ForegroundColor Green
        Write-Host "Asegúrate de que el backend esté corriendo en http://127.0.0.1:8000`n" -ForegroundColor Yellow

        # Verificar si el backend está corriendo
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "✅ Backend detectado y corriendo" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ ADVERTENCIA: No se pudo conectar al backend" -ForegroundColor Yellow
            Write-Host "   Inicia el backend con: cd backend; uvicorn app.main:app --reload`n" -ForegroundColor Yellow
            $continuar = Read-Host "¿Continuar de todos modos? (s/n)"
            if ($continuar -ne "s") { exit 0 }
        }

        cd backend
        python -m pytest tests/e2e/ -v -k "test_api" --tb=short
    }

    "2" {
        Write-Host "`n🎨 Ejecutando Tests de UI..." -ForegroundColor Green
        Write-Host "Asegúrate de que:" -ForegroundColor Yellow
        Write-Host "  - Backend esté corriendo en http://127.0.0.1:8000" -ForegroundColor Yellow
        Write-Host "  - Frontend esté corriendo en http://localhost:5173`n" -ForegroundColor Yellow

        # Verificar backend
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "✅ Backend detectado" -ForegroundColor Green
        } catch {
            Write-Host "❌ Backend NO detectado. Inicia con: cd backend; uvicorn app.main:app --reload" -ForegroundColor Red
            exit 1
        }

        # Verificar frontend
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5173/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "✅ Frontend detectado" -ForegroundColor Green
        } catch {
            Write-Host "❌ Frontend NO detectado. Inicia con: cd frontend_t; npm run dev" -ForegroundColor Red
            exit 1
        }

        Write-Host "`n🚀 Ejecutando tests de UI..." -ForegroundColor Cyan
        cd backend
        python -m pytest tests/e2e/ -v -k "test_ui" --tb=short
    }

    "3" {
        Write-Host "`n🌟 Ejecutando TODOS los Tests E2E..." -ForegroundColor Green
        Write-Host "Verificando servicios...`n" -ForegroundColor Yellow

        # Verificar backend
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "✅ Backend corriendo" -ForegroundColor Green
        } catch {
            Write-Host "❌ Backend NO corriendo. Inicia con: cd backend; uvicorn app.main:app --reload" -ForegroundColor Red
            exit 1
        }

        # Verificar frontend
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5173/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "✅ Frontend corriendo" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Frontend NO corriendo. Los tests de UI fallarán." -ForegroundColor Yellow
            Write-Host "   Inicia con: cd frontend_t; npm run dev" -ForegroundColor Yellow
        }

        Write-Host "`n🚀 Ejecutando todos los tests..." -ForegroundColor Cyan
        cd backend
        python -m pytest tests/e2e/ -v --tb=short
    }

    "4" {
        Write-Host "`n🔍 Verificando servicios...`n" -ForegroundColor Cyan

        # Verificar Backend
        Write-Host "Backend (http://127.0.0.1:8000):" -ForegroundColor White
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "  ✅ Corriendo" -ForegroundColor Green
            Write-Host "  Respuesta: $($response.StatusCode)" -ForegroundColor Gray
        } catch {
            Write-Host "  ❌ NO corriendo" -ForegroundColor Red
            Write-Host "  Comando para iniciar: cd backend; uvicorn app.main:app --reload" -ForegroundColor Yellow
        }

        # Verificar Frontend
        Write-Host "`nFrontend (http://localhost:5173):" -ForegroundColor White
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5173/" -TimeoutSec 2 -UseBasicParsing
            Write-Host "  ✅ Corriendo" -ForegroundColor Green
            Write-Host "  Respuesta: $($response.StatusCode)" -ForegroundColor Gray
        } catch {
            Write-Host "  ❌ NO corriendo" -ForegroundColor Red
            Write-Host "  Comando para iniciar: cd frontend_t; npm run dev" -ForegroundColor Yellow
        }

        # Verificar Playwright
        Write-Host "`nPlaywright:" -ForegroundColor White
        cd backend
        $playwrightCheck = python -c "try:`n    import playwright`n    print('instalado')`nexcept:`n    print('no instalado')" 2>$null
        if ($playwrightCheck -eq "instalado") {
            Write-Host "  ✅ Instalado" -ForegroundColor Green
        } else {
            Write-Host "  ❌ NO instalado" -ForegroundColor Red
            Write-Host "  Comando para instalar: pip install playwright pytest-playwright; playwright install chromium" -ForegroundColor Yellow
        }
        cd ..
    }

    "5" {
        Write-Host "`n📦 Instalando dependencias E2E..." -ForegroundColor Cyan

        cd backend

        Write-Host "`n1️⃣ Instalando requests..." -ForegroundColor Yellow
        pip install requests

        Write-Host "`n2️⃣ Instalando playwright y pytest-playwright..." -ForegroundColor Yellow
        pip install playwright pytest-playwright

        Write-Host "`n3️⃣ Instalando navegadores de Playwright..." -ForegroundColor Yellow
        playwright install chromium

        Write-Host "`n✅ Dependencias E2E instaladas correctamente" -ForegroundColor Green
        cd ..
    }

    "6" {
        Write-Host "`nSaliendo..." -ForegroundColor Gray
        exit 0
    }

    default {
        Write-Host "`n❌ Opción inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✨ Proceso completado" -ForegroundColor Green

