# NeoCare Mobile - Implementación Completa Flutter

## 📱 Proyecto Creado

Se ha creado una aplicación móvil Flutter completa para NeoCare Health en la rama `feature/fluttermobile`.

## ✅ Archivos Creados

### Configuración del Proyecto
- ✅ `pubspec.yaml` - Dependencias y configuración del proyecto
- ✅ `analysis_options.yaml` - Reglas de linting
- ✅ `.gitignore` - Archivos excluidos de Git
- ✅ `README.md` - Documentación completa (instalación, uso, troubleshooting)
- ✅ `QUICK_START.md` - Guía rápida de inicio
- ✅ `build-apk.ps1` - Script automatizado para compilar APK

### Código Fuente (lib/)

#### Punto de Entrada
- ✅ `lib/main.dart` - App principal con Provider, Material 3, Splash screen

#### Configuración
- ✅ `lib/config/api_config.dart` - URL del backend (10.0.2.2 para emulador)

#### Modelos de Datos
- ✅ `lib/models/user.dart` - Modelo de Usuario
- ✅ `lib/models/board.dart` - Modelos de Board y BoardList
- ✅ `lib/models/card.dart` - Modelo de Tarjeta con labels y subtasks
- ✅ `lib/models/label.dart` - Modelo de Etiqueta con colores predefinidos
- ✅ `lib/models/subtask.dart` - Modelo de Subtarea con estado completed

#### Servicios
- ✅ `lib/services/api_service.dart` - Cliente HTTP completo:
  - Auth: register(), login(), logout(), loadToken()
  - Boards: getBoards(), createBoard(), getBoardLists()
  - Cards: getCards(), getCard(), createCard(), updateCard(), deleteCard()
  - Labels: getCardLabels(), addLabel(), deleteLabel()
  - Subtasks: getCardSubtasks(), addSubtask(), updateSubtask(), deleteSubtask()

#### Pantallas
- ✅ `lib/screens/login_screen.dart` - Login y Registro con validación
- ✅ `lib/screens/boards_screen.dart` - Vista Kanban horizontal con búsqueda
- ✅ `lib/screens/card_detail_screen.dart` - Detalle completo de tarjeta

#### Widgets Reutilizables
- ✅ `lib/widgets/card_item.dart` - Tarjeta compacta con labels y progreso
- ✅ `lib/widgets/label_chip.dart` - Chip de etiqueta con color
- ✅ `lib/widgets/subtask_item.dart` - Item de subtarea con checkbox

### Configuración Android

#### Estructura Android
- ✅ `android/build.gradle` - Configuración raíz de Gradle
- ✅ `android/settings.gradle` - Plugin management Flutter
- ✅ `android/gradle/wrapper/gradle-wrapper.properties` - Gradle 7.5
- ✅ `android/app/build.gradle` - Configuración de la app:
  - namespace: com.neocare.mobile
  - compileSdk: 34
  - minSdk: 21
  - targetSdk: 34
  - Release build con minification

#### Código Nativo
- ✅ `android/app/src/main/kotlin/com/neocare/mobile/MainActivity.kt` - Activity principal
- ✅ `android/app/src/main/AndroidManifest.xml` - Permisos y configuración:
  - INTERNET permission
  - ACCESS_NETWORK_STATE permission
  - App name: "NeoCare Health"

## 🎨 Funcionalidades Implementadas

### Autenticación
- [x] Pantalla de Login y Registro
- [x] Validación de formularios
- [x] Persistencia de token con SharedPreferences
- [x] Splash screen con verificación automática de sesión
- [x] Logout

### Tablero Kanban
- [x] Vista horizontal de listas (scrollable)
- [x] Visualización de tarjetas por lista
- [x] Búsqueda de tarjetas
- [x] Creación rápida de tarjetas
- [x] Pull to refresh
- [x] Contador de tarjetas por lista

### Gestión de Tarjetas
- [x] Ver detalle completo de tarjeta
- [x] Editar título y descripción
- [x] Auto-guardado al editar

### Labels (Etiquetas)
- [x] Visualización de labels en tarjetas
- [x] Añadir labels con selector de color
- [x] Colores predefinidos (Urgente, Media, Baja, Feature, QA, Bloqueado)
- [x] Selector de color personalizado (ColorPicker)
- [x] Eliminar labels
- [x] Labels compactos en vista de lista

### Subtasks (Subtareas)
- [x] Lista de subtareas en detalle de tarjeta
- [x] Añadir subtareas
- [x] Marcar como completada/pendiente (checkbox)
- [x] Eliminar subtareas con confirmación
- [x] Barra de progreso visual
- [x] Contador de subtareas completadas
- [x] Indicador de progreso en vista de lista

### UI/UX
- [x] Material Design 3
- [x] Tema con color scheme
- [x] Iconografía coherente
- [x] Loading states (CircularProgressIndicator)
- [x] Error handling
- [x] Snackbars para feedback
- [x] Dialogs para confirmaciones
- [x] Responsive layout

## 📦 Dependencias Utilizadas

```yaml
http: ^1.1.0                      # Cliente HTTP para API REST
provider: ^6.1.1                  # State management
shared_preferences: ^2.2.2        # Almacenamiento local (token)
flutter_colorpicker: ^1.0.3       # Selector de colores para labels
intl: ^0.18.1                     # Formateo de fechas
flutter_svg: ^2.0.9               # Soporte para SVG
```

## 🔧 Configuración Backend

La app está configurada para conectarse al backend FastAPI:

- **Emulador Android**: `http://10.0.2.2:8000`
- **Dispositivo físico**: Necesita IP local (ej: `http://192.168.1.X:8000`)

### Endpoints Consumidos

- POST `/auth/register` - Registro de usuarios
- POST `/auth/login` - Login (devuelve JWT token)
- GET `/boards` - Listar boards
- POST `/boards` - Crear board
- GET `/boards/{id}/lists` - Listar listas de un board
- GET `/cards` - Listar tarjetas (con filtros search, responsible_id, list_id)
- GET `/cards/{id}` - Obtener tarjeta específica
- POST `/cards` - Crear tarjeta
- PUT `/cards/{id}` - Actualizar tarjeta
- DELETE `/cards/{id}` - Eliminar tarjeta
- GET `/cards/{id}/labels` - Listar labels de tarjeta
- POST `/cards/{id}/labels` - Añadir label
- DELETE `/cards/labels/{id}` - Eliminar label
- GET `/cards/{id}/subtasks` - Listar subtasks
- POST `/cards/{id}/subtasks` - Añadir subtask
- PATCH `/cards/subtasks/{id}` - Actualizar subtask (toggle completed)
- DELETE `/cards/subtasks/{id}` - Eliminar subtask

## 🚀 Cómo Usar

### 1. Instalar Flutter

Descarga Flutter SDK desde: https://docs.flutter.dev/get-started/install/windows

```powershell
# Agregar al PATH
flutter --version
flutter doctor
```

### 2. Instalar Dependencias

```powershell
cd frontend_mobile
flutter pub get
```

### 3. Iniciar Backend

```powershell
cd ..\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Ejecutar App

```powershell
# En emulador
flutter emulators --launch pixel_5
flutter run

# O en dispositivo físico (conectado por USB)
flutter run
```

### 5. Generar APK

```powershell
# Opción 1: Usar script automatizado
.\build-apk.ps1 release

# Opción 2: Comando directo
flutter build apk --release

# Opción 3: APK optimizado por arquitectura
flutter build apk --split-per-abi
```

APK generado en: `build\app\outputs\flutter-apk\`

## 📁 Estructura de Directorios

```
frontend_mobile/
├── lib/
│   ├── main.dart                           # Punto de entrada
│   ├── config/
│   │   └── api_config.dart                # Configuración API
│   ├── models/
│   │   ├── user.dart                      # Modelo Usuario
│   │   ├── board.dart                     # Modelos Board/BoardList
│   │   ├── card.dart                      # Modelo Tarjeta
│   │   ├── label.dart                     # Modelo Etiqueta
│   │   └── subtask.dart                   # Modelo Subtarea
│   ├── services/
│   │   └── api_service.dart               # Cliente HTTP
│   ├── screens/
│   │   ├── login_screen.dart              # Login/Registro
│   │   ├── boards_screen.dart             # Tablero Kanban
│   │   └── card_detail_screen.dart        # Detalle de tarjeta
│   └── widgets/
│       ├── card_item.dart                 # Widget tarjeta
│       ├── label_chip.dart                # Widget etiqueta
│       └── subtask_item.dart              # Widget subtarea
├── android/
│   ├── app/
│   │   ├── build.gradle                   # Config Android
│   │   └── src/main/
│   │       ├── AndroidManifest.xml        # Permisos
│   │       └── kotlin/com/neocare/mobile/
│   │           └── MainActivity.kt         # Activity principal
│   ├── build.gradle                       # Config raíz
│   └── settings.gradle                    # Plugin management
├── pubspec.yaml                            # Dependencias
├── analysis_options.yaml                   # Linting
├── .gitignore                             # Git ignore
├── README.md                              # Documentación completa
├── QUICK_START.md                         # Guía rápida
└── build-apk.ps1                          # Script build APK
```

## 🎯 Características Técnicas

### State Management
- Provider para inyección de dependencias (ApiService)
- setState local para estado de UI

### Persistencia
- SharedPreferences para JWT token
- No hay caché offline (próxima mejora)

### HTTP Client
- Package `http` para requests REST
- Headers con Authorization Bearer token
- JSON encoding/decoding

### Routing
- MaterialPageRoute para navegación
- Navigator.push/pop
- pushReplacement para login/splash

### Tema
- Material 3 con ColorScheme.fromSeed
- Primary color: Blue
- Cards con elevación y border radius
- Input fields con OutlineInputBorder

## 🐛 Troubleshooting

### Flutter no reconocido
```powershell
# Agrega al PATH de Windows
flutter doctor
```

### Gradle build failed
```powershell
cd android
.\gradlew clean
cd ..
flutter clean
flutter pub get
```

### No se conecta al backend
- Verifica que backend esté en `http://localhost:8000`
- Para emulador: usa `http://10.0.2.2:8000`
- Para físico: usa tu IP local (`ipconfig` para obtenerla)
- Verifica firewall no bloquee puerto 8000

### APK no instala
```powershell
# Ver logs
adb logcat | Select-String "flutter"

# Reinstalar
adb uninstall com.neocare.mobile
adb install build\app\outputs\flutter-apk\app-release.apk
```

## 📝 Notas Importantes

1. **Flutter SDK requerido**: El proyecto está listo pero necesitas instalar Flutter para compilar
2. **Backend debe estar corriendo**: La app consume API REST del backend FastAPI
3. **Permisos Android**: INTERNET y ACCESS_NETWORK_STATE ya configurados
4. **API URL**: Cambia en `lib/config/api_config.dart` según tu entorno
5. **Emulador vs Físico**: Emulador usa `10.0.2.2`, físico necesita IP local

## 🔜 Próximas Mejoras Sugeridas

- [ ] Modo offline con SQLite local
- [ ] Notificaciones push
- [ ] Drag & drop para mover tarjetas entre listas
- [ ] Modo oscuro
- [ ] WebSockets para sync en tiempo real
- [ ] Worklogs/Time tracking
- [ ] Filtros avanzados con bottom sheet
- [ ] Exportar datos (PDF, Excel)
- [ ] Imagen de perfil
- [ ] Colaboración multi-usuario
- [ ] Archivos adjuntos en tarjetas
- [ ] Comentarios en tarjetas

## ✨ Estado del Proyecto

**✅ PROYECTO COMPLETO Y LISTO PARA COMPILAR**

- [x] Código fuente Flutter completo
- [x] Configuración Android
- [x] Dependencias configuradas
- [x] Documentación completa
- [x] Scripts de build
- [x] Conexión con backend configurada
- [x] Todas las funcionalidades de Semana 6 implementadas

**Siguiente paso**: Instalar Flutter SDK y ejecutar `flutter pub get` para compilar la app.

---

**Rama Git**: `feature/fluttermobile`  
**Commit sugerido**: "feat: Implementación completa de app móvil Flutter con Labels y Subtasks"
