# Flutter Mobile - NeoCare Health

## Inicio Rápido

### 1. Instalar Flutter (si no lo tienes)

#### Windows:
```powershell
# Descarga Flutter SDK
# https://docs.flutter.dev/get-started/install/windows

# Agrega al PATH:
# C:\src\flutter\bin

# Verifica instalación
flutter doctor
```

### 2. Instalar Dependencias

```powershell
cd frontend_mobile
flutter pub get
```

### 3. Configurar Backend

Edita `lib/config/api_config.dart`:
- Emulador Android: `http://10.0.2.2:8000`
- Dispositivo físico: `http://TU_IP:8000`

### 4. Ejecutar

```powershell
# Iniciar backend (otra terminal)
cd ..\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0

# Ejecutar app
cd ..\frontend_mobile
flutter run
```

### 5. Generar APK

```powershell
# APK de prueba
flutter build apk --debug

# APK de producción
flutter build apk --release

# APK optimizado por arquitectura (recomendado)
flutter build apk --split-per-abi
```

APK se genera en: `build\app\outputs\flutter-apk\`

## Comandos Útiles

```powershell
# Ver dispositivos conectados
flutter devices

# Ver logs
flutter logs

# Limpiar build
flutter clean

# Actualizar dependencias
flutter pub upgrade

# Ejecutar en dispositivo específico
flutter run -d DEVICE_ID
```

## Estructura

- `lib/main.dart` - Entrada de la app
- `lib/screens/` - Pantallas (Login, Boards, CardDetail)
- `lib/widgets/` - Componentes reutilizables
- `lib/services/api_service.dart` - Cliente HTTP
- `lib/models/` - Modelos de datos
- `lib/config/` - Configuración de la API

## Troubleshooting

**No se conecta al backend:**
- Verifica que el backend esté corriendo
- Usa `10.0.2.2` para emulador, no `localhost`
- Para físico, usa tu IP local (obtén con `ipconfig`)

**Gradle build failed:**
```powershell
cd android
.\gradlew clean
cd ..
flutter clean
flutter pub get
```

Ver [README.md](README.md) para documentación completa.
