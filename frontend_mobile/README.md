# NeoCare Health - Mobile App (Flutter)

Aplicación móvil nativa para NeoCare Health, desarrollada en Flutter para Android.

## 🚀 Características

- ✅ Autenticación (Login/Registro)
- ✅ Visualización de tableros Kanban
- ✅ Gestión de tarjetas con Labels y Subtasks
- ✅ Búsqueda y filtrado de tarjetas
- ✅ Progreso visual de subtareas
- ✅ Selector de colores para etiquetas
- ✅ Interfaz Material Design 3
- ✅ Conexión con API FastAPI del backend

## 📋 Requisitos Previos

### 1. Instalar Flutter

#### Windows:
1. Descarga Flutter SDK desde: https://docs.flutter.dev/get-started/install/windows
2. Extrae el archivo en `C:\src\flutter` (o tu ubicación preferida)
3. Agrega Flutter al PATH:
   - Busca "Variables de entorno" en Windows
   - Edita la variable `Path`
   - Añade `C:\src\flutter\bin`

4. Verifica la instalación:
```powershell
flutter --version
flutter doctor
```

### 2. Instalar Android Studio

1. Descarga desde: https://developer.android.com/studio
2. Instala Android Studio
3. Abre Android Studio → Tools → SDK Manager
4. Instala:
   - Android SDK Platform (API 34)
   - Android SDK Build-Tools
   - Android Emulator

### 3. Configurar Variables de Entorno

```powershell
# Android SDK
$env:ANDROID_HOME = "C:\Users\TU_USUARIO\AppData\Local\Android\Sdk"
$env:Path += ";$env:ANDROID_HOME\platform-tools"
$env:Path += ";$env:ANDROID_HOME\cmdline-tools\latest\bin"
```

### 4. Aceptar Licencias Android

```powershell
flutter doctor --android-licenses
```

## 🔧 Configuración del Proyecto

### 1. Instalar Dependencias

Navega a la carpeta del proyecto móvil:

```powershell
cd frontend_mobile
flutter pub get
```

### 2. Configurar la URL del Backend

Edita `lib/config/api_config.dart`:

```dart
static const String baseUrl = 'http://10.0.2.2:8000';  // Emulador Android
// O para dispositivo físico:
// static const String baseUrl = 'http://TU_IP_LOCAL:8000';
```

**Obtener tu IP local:**
```powershell
ipconfig
# Busca "Dirección IPv4" en tu adaptador de red principal
```

### 3. Iniciar el Backend

En otra terminal, inicia el servidor FastAPI:

```powershell
cd ..\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📱 Ejecutar la Aplicación

### Opción 1: Emulador Android

1. **Crear un emulador:**
```powershell
# Lista los dispositivos disponibles
flutter emulators

# Crea un nuevo emulador (si no tienes)
flutter emulators --create --name pixel_5
```

2. **Iniciar el emulador:**
```powershell
flutter emulators --launch pixel_5
```

3. **Ejecutar la app:**
```powershell
flutter run
```

### Opción 2: Dispositivo Físico

1. **Habilita "Opciones de Desarrollador" en tu Android:**
   - Ve a Ajustes → Acerca del teléfono
   - Toca "Número de compilación" 7 veces
   - Regresa y entra a "Opciones de desarrollador"
   - Activa "Depuración USB"

2. **Conecta tu teléfono por USB**

3. **Verifica que esté detectado:**
```powershell
flutter devices
```

4. **Ejecutar la app:**
```powershell
flutter run
```

## 🏗️ Generar APK para Instalación

### APK de Depuración (Debug)

```powershell
flutter build apk --debug
```

El APK se generará en: `build\app\outputs\flutter-apk\app-debug.apk`

### APK de Producción (Release)

```powershell
flutter build apk --release
```

El APK se generará en: `build\app\outputs\flutter-apk\app-release.apk`

### APK Optimizado por Arquitectura

Para generar APKs más pequeños (uno por cada tipo de procesador):

```powershell
flutter build apk --split-per-abi
```

Esto genera:
- `app-armeabi-v7a-release.apk` (ARM 32-bit)
- `app-arm64-v8a-release.apk` (ARM 64-bit) ← Más común
- `app-x86_64-release.apk` (Intel 64-bit)

## 📦 Instalar APK en Dispositivo

### Método 1: Desde el PC (ADB)

```powershell
# Con el dispositivo conectado por USB
flutter install
# O directamente con adb:
adb install build\app\outputs\flutter-apk\app-release.apk
```

### Método 2: Transferir el APK

1. Copia el APK al teléfono (por cable, Drive, etc.)
2. Abre el archivo APK desde el explorador del teléfono
3. Permite "Instalar desde fuentes desconocidas" si te lo pide
4. Instala la aplicación

## 🎨 Estructura del Proyecto

```
frontend_mobile/
├── lib/
│   ├── main.dart                    # Punto de entrada de la app
│   ├── config/
│   │   └── api_config.dart         # Configuración de la API
│   ├── models/
│   │   ├── user.dart               # Modelo de Usuario
│   │   ├── board.dart              # Modelos de Board y BoardList
│   │   ├── card.dart               # Modelo de Tarjeta
│   │   ├── label.dart              # Modelo de Etiqueta
│   │   └── subtask.dart            # Modelo de Subtarea
│   ├── services/
│   │   └── api_service.dart        # Cliente HTTP para el backend
│   ├── screens/
│   │   ├── login_screen.dart       # Pantalla de Login/Registro
│   │   ├── boards_screen.dart      # Vista del tablero Kanban
│   │   └── card_detail_screen.dart # Detalle de tarjeta
│   └── widgets/
│       ├── card_item.dart          # Widget de tarjeta
│       ├── label_chip.dart         # Widget de etiqueta
│       └── subtask_item.dart       # Widget de subtarea
├── android/                         # Configuración Android
├── pubspec.yaml                     # Dependencias del proyecto
└── README.md                        # Este archivo
```

## 🔑 Funcionalidades Principales

### Login y Registro
- Formulario de autenticación
- Validación de campos
- Persistencia de token (SharedPreferences)
- Splash screen con verificación automática

### Tablero Kanban
- Vista horizontal de listas
- Tarjetas con título, etiquetas y progreso
- Búsqueda de tarjetas
- Pull to refresh
- Creación rápida de tarjetas

### Detalle de Tarjeta
- Edición de título y descripción
- Gestión de etiquetas con selector de color
- Gestión de subtareas con checkbox
- Barra de progreso visual
- Auto-guardado

## 🐛 Solución de Problemas

### Error: "Unable to locate adb"
```powershell
flutter doctor
# Sigue las instrucciones para instalar Android SDK
```

### Error: "Gradle build failed"
```powershell
cd android
.\gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### Error: "No connected devices"
- Para emulador: Asegúrate de que esté ejecutándose
- Para físico: Verifica que la depuración USB esté habilitada

### No se conecta al backend
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Para emulador: Usa `http://10.0.2.2:8000`
- Para físico: Usa tu IP local (ej: `http://192.168.1.X:8000`)
- Verifica que no haya firewall bloqueando el puerto 8000

### APK se instala pero no abre
```powershell
# Ver logs en tiempo real
adb logcat | Select-String "flutter"
```

## 📚 Dependencias Utilizadas

- **http**: Cliente HTTP para consumir la API
- **provider**: State management
- **shared_preferences**: Almacenamiento local del token
- **flutter_colorpicker**: Selector de colores para etiquetas
- **intl**: Formateo de fechas

## 🎯 Próximas Mejoras

- [ ] Modo offline con caché local
- [ ] Notificaciones push
- [ ] Arrastrar y soltar tarjetas
- [ ] Modo oscuro
- [ ] Sincronización en tiempo real (WebSockets)
- [ ] Worklogs/Time tracking
- [ ] Filtros avanzados
- [ ] Exportar datos

## 📄 Licencia

Este proyecto es parte de NeoCare Health.

## 👥 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.
