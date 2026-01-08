# Script para compilar APK de NeoCare Mobile
# Uso: .\build-apk.ps1 [debug|release|split]

param(
    [Parameter(Position=0)]
    [ValidateSet('debug', 'release', 'split')]
    [string]$BuildType = 'release'
)

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  NeoCare Mobile - Build APK" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Flutter esté instalado
try {
    $flutterVersion = flutter --version 2>&1 | Select-String "Flutter" | Select-Object -First 1
    Write-Host "✓ Flutter detectado: $flutterVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Flutter no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "  Instala Flutter desde: https://docs.flutter.dev/get-started/install" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Limpiar build anterior
Write-Host "Limpiando builds anteriores..." -ForegroundColor Yellow
flutter clean
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Error en flutter clean" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Limpieza completada" -ForegroundColor Green
Write-Host ""

# Obtener dependencias
Write-Host "Obteniendo dependencias..." -ForegroundColor Yellow
flutter pub get
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Error obteniendo dependencias" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
Write-Host ""

# Compilar APK según el tipo
Write-Host "Compilando APK ($BuildType)..." -ForegroundColor Yellow
Write-Host ""

switch ($BuildType) {
    'debug' {
        flutter build apk --debug
        $apkPath = "build\app\outputs\flutter-apk\app-debug.apk"
    }
    'release' {
        flutter build apk --release
        $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
    }
    'split' {
        flutter build apk --split-per-abi --release
        Write-Host ""
        Write-Host "APKs generados por arquitectura:" -ForegroundColor Cyan
        Write-Host "  - app-armeabi-v7a-release.apk (ARM 32-bit)" -ForegroundColor White
        Write-Host "  - app-arm64-v8a-release.apk (ARM 64-bit) ← Recomendado" -ForegroundColor White
        Write-Host "  - app-x86_64-release.apk (Intel 64-bit)" -ForegroundColor White
        $apkPath = "build\app\outputs\flutter-apk\"
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ Error al compilar APK" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "  ✓ APK compilado exitosamente!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Mostrar ubicación del APK
if (Test-Path $apkPath) {
    $fullPath = Resolve-Path $apkPath
    Write-Host "Ubicación: $fullPath" -ForegroundColor Cyan
    
    # Mostrar tamaño
    if ($BuildType -eq 'split') {
        Get-ChildItem "$apkPath*.apk" | ForEach-Object {
            $sizeMB = [math]::Round($_.Length / 1MB, 2)
            Write-Host "  $($_.Name): $sizeMB MB" -ForegroundColor White
        }
    } else {
        $sizeMB = [math]::Round((Get-Item $apkPath).Length / 1MB, 2)
        Write-Host "Tamaño: $sizeMB MB" -ForegroundColor White
    }
} else {
    Write-Host "⚠ No se pudo encontrar el APK en la ubicación esperada" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  Próximos pasos:" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Transferir el APK a tu dispositivo Android" -ForegroundColor White
Write-Host "2. Habilitar 'Instalar desde fuentes desconocidas'" -ForegroundColor White
Write-Host "3. Abrir el APK e instalar" -ForegroundColor White
Write-Host ""
Write-Host "O instalar directamente con ADB:" -ForegroundColor White
Write-Host "  adb install $apkPath" -ForegroundColor Yellow
Write-Host ""

# Preguntar si instalar automáticamente
Write-Host "¿Deseas instalar el APK ahora en un dispositivo conectado? (S/N): " -NoNewline -ForegroundColor Cyan
$response = Read-Host

if ($response -eq 'S' -or $response -eq 's') {
    Write-Host ""
    Write-Host "Verificando dispositivos conectados..." -ForegroundColor Yellow
    
    $devices = adb devices 2>&1
    if ($devices -match "device$") {
        Write-Host "✓ Dispositivo detectado" -ForegroundColor Green
        Write-Host "Instalando APK..." -ForegroundColor Yellow
        
        if ($BuildType -eq 'split') {
            # Para split, instalar el ARM64 (más común)
            $arm64Apk = Join-Path $apkPath "app-arm64-v8a-release.apk"
            if (Test-Path $arm64Apk) {
                adb install -r $arm64Apk
            } else {
                Write-Host "⚠ No se encontró app-arm64-v8a-release.apk" -ForegroundColor Yellow
            }
        } else {
            adb install -r $apkPath
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ APK instalado exitosamente" -ForegroundColor Green
        } else {
            Write-Host "✗ Error al instalar APK" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ No se detectó ningún dispositivo Android conectado" -ForegroundColor Red
        Write-Host "  Conecta tu dispositivo y asegúrate de tener la depuración USB habilitada" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "¡Listo! 🚀" -ForegroundColor Green
