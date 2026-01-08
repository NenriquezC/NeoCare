# ✅ CHECKLIST - Primera Ejecución de NeoCare Mobile

## 📋 Antes de Empezar

### ¿Qué tengo hasta ahora?
- ✅ Código fuente completo de la app Flutter
- ✅ Configuración Android lista
- ✅ Documentación completa
- ✅ Backend FastAPI funcionando (Semana 6 completa)

### ¿Qué me falta?
- ❌ Flutter SDK instalado en mi computadora
- ❌ Android Studio (o Android SDK standalone)
- ❌ Compilar el proyecto

---

## 🚀 PASOS PARA PRIMERA EJECUCIÓN

### PASO 1: Instalar Flutter (15-30 minutos)

1. **Descargar Flutter SDK**
   - URL: https://docs.flutter.dev/get-started/install/windows
   - Archivo: `flutter_windows_X.X.X-stable.zip`
   - Tamaño: ~1.5 GB

2. **Extraer Flutter**
   ```powershell
   # Extraer en C:\src\flutter (o donde prefieras)
   # NO extraer en Program Files (necesita permisos)
   ```

3. **Agregar Flutter al PATH**
   - Presiona `Win + R` → escribe `sysdm.cpl` → Enter
   - Pestaña "Opciones Avanzadas"
   - Click en "Variables de entorno"
   - En "Variables del sistema" → selecciona "Path" → "Editar"
   - Click "Nuevo" → agrega: `C:\src\flutter\bin`
   - Click "Aceptar" en todas las ventanas

4. **Verificar instalación**
   ```powershell
   # Abre una NUEVA terminal PowerShell
   flutter --version
   
   # Debería mostrar:
   # Flutter 3.X.X • channel stable • ...
   ```

---

### PASO 2: Instalar Android Studio (30-45 minutos)

1. **Descargar Android Studio**
   - URL: https://developer.android.com/studio
   - Tamaño: ~1 GB

2. **Instalar Android Studio**
   - Ejecuta el instalador
   - Acepta configuración por defecto
   - Espera a que descargue componentes (puede tardar)

3. **Configurar Android SDK**
   - Abre Android Studio
   - Click en "More Actions" → "SDK Manager"
   - En "SDK Platforms" marca:
     - ✅ Android 14.0 (API 34)
   - En "SDK Tools" marca:
     - ✅ Android SDK Build-Tools
     - ✅ Android SDK Command-line Tools
     - ✅ Android Emulator
     - ✅ Android SDK Platform-Tools
   - Click "Apply" → Espera la descarga

4. **Aceptar licencias**
   ```powershell
   flutter doctor --android-licenses
   # Presiona 'y' para aceptar todas
   ```

5. **Verificar configuración**
   ```powershell
   flutter doctor
   
   # Deberías ver checkmarks (✓) en:
   # [✓] Flutter
   # [✓] Android toolchain
   # [!] Chrome (opcional, solo para web)
   # [!] Visual Studio (opcional, solo para Windows desktop)
   ```

---

### PASO 3: Configurar Emulador o Dispositivo

#### OPCIÓN A: Emulador Android (recomendado para desarrollo)

1. **Crear emulador**
   ```powershell
   cd frontend_mobile
   flutter emulators
   # Si no hay ninguno:
   flutter emulators --create
   ```

2. **O desde Android Studio:**
   - Tools → Device Manager
   - Click "Create Device"
   - Elige "Pixel 5" → Next
   - Descarga imagen de sistema (API 34 recomendado)
   - Finish

3. **Iniciar emulador**
   ```powershell
   flutter emulators --launch <nombre_emulador>
   ```

#### OPCIÓN B: Dispositivo Físico Android

1. **Habilitar modo desarrollador en tu teléfono:**
   - Ajustes → Acerca del teléfono
   - Toca "Número de compilación" 7 veces
   - Aparecerá "Ahora eres desarrollador"

2. **Activar depuración USB:**
   - Ajustes → Opciones de desarrollador
   - Activa "Depuración USB"

3. **Conectar por USB y verificar:**
   ```powershell
   flutter devices
   # Deberías ver tu dispositivo listado
   ```

---

### PASO 4: Iniciar Backend

```powershell
# Terminal 1 - Backend
cd C:\Users\usuario\Documents\NeoCare\backend

# Activar entorno virtual (si usas .venv)
.\.venv\Scripts\Activate.ps1

# Iniciar servidor en 0.0.0.0 para que sea accesible desde móvil
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Deberías ver:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**⚠️ IMPORTANTE**: El backend DEBE estar en `0.0.0.0`, no solo en `127.0.0.1`

---

### PASO 5: Configurar URL de API (solo si usas dispositivo físico)

Si usas **emulador**, ya está configurado (`http://10.0.2.2:8000`). **Salta este paso**.

Si usas **dispositivo físico**:

1. **Obtén tu IP local:**
   ```powershell
   ipconfig
   # Busca "Dirección IPv4" en tu adaptador Wi-Fi o Ethernet
   # Ejemplo: 192.168.1.100
   ```

2. **Edita la configuración:**
   ```powershell
   # Abre: frontend_mobile\lib\config\api_config.dart
   # Cambia:
   static const String baseUrl = 'http://TU_IP_LOCAL:8000';
   # Ejemplo:
   static const String baseUrl = 'http://192.168.1.100:8000';
   ```

3. **Verifica conectividad:**
   - Asegúrate de que PC y teléfono estén en la MISMA red Wi-Fi
   - Desactiva firewall temporalmente si tienes problemas

---

### PASO 6: Instalar Dependencias Flutter

```powershell
# Terminal 2 - Flutter App
cd C:\Users\usuario\Documents\NeoCare\frontend_mobile

# Instalar dependencias
flutter pub get

# Deberías ver:
# Running "flutter pub get" in frontend_mobile...
# Got dependencies!
```

---

### PASO 7: Ejecutar la App (¡MOMENTO DE LA VERDAD!)

```powershell
# Con emulador o dispositivo conectado
flutter run

# Primera vez tardará más (compila todo)
# Verás output tipo:
# Launching lib\main.dart on Pixel 5 in debug mode...
# Running Gradle task 'assembleDebug'...
# ✓ Built build\app\outputs\flutter-apk\app-debug.apk
# Installing build\app\outputs\flutter-apk\app-debug.apk...
# Syncing files to device Pixel 5...
# 
# 🔥  To hot reload changes while running, press "r" or "R".
# For a more detailed help message, press "h". To quit, press "q".
```

**🎉 Si ves esto, ¡LA APP ESTÁ CORRIENDO!**

---

## ✅ VERIFICACIÓN DE FUNCIONAMIENTO

### 1. Pantalla de Login
- [ ] Se ve la pantalla de login con logo de NeoCare
- [ ] Campos: Email, Contraseña
- [ ] Botón "Iniciar Sesión"
- [ ] Link "¿No tienes cuenta? Regístrate"

### 2. Registro de Usuario
- [ ] Click en "Regístrate"
- [ ] Campos: Email, Nombre, Contraseña
- [ ] Crear un usuario de prueba
- [ ] Ver mensaje "Registro exitoso"

### 3. Login
- [ ] Iniciar sesión con el usuario creado
- [ ] Ver pantalla de Boards

### 4. Tablero Kanban
- [ ] Se ve el tablero horizontal con listas
- [ ] Click en "+" para crear tarjeta
- [ ] Se crea la tarjeta y aparece en la lista

### 5. Detalle de Tarjeta
- [ ] Click en una tarjeta
- [ ] Editar título y descripción
- [ ] Click en "+" junto a "Etiquetas"
- [ ] Crear etiqueta con color
- [ ] Ver la etiqueta en la tarjeta
- [ ] Click en "+" junto a "Subtareas"
- [ ] Crear subtarea
- [ ] Marcar checkbox de subtarea
- [ ] Ver barra de progreso actualizada

### 6. Búsqueda
- [ ] Click en icono de búsqueda (🔍)
- [ ] Escribir texto
- [ ] Ver tarjetas filtradas

**Si todo funciona → ✅ ¡APP COMPLETAMENTE FUNCIONAL!**

---

## 🏗️ GENERAR APK PARA INSTALACIÓN

### Una vez que todo funcione correctamente:

```powershell
# Opción 1: Usar script automatizado
.\build-apk.ps1 release

# Opción 2: Comando manual
flutter build apk --release

# Opción 3: APK optimizado (recomendado)
flutter build apk --split-per-abi
```

**APK generado en:**
```
frontend_mobile\build\app\outputs\flutter-apk\
├── app-release.apk              (Universal)
├── app-arm64-v8a-release.apk    (64-bit ARM - mayoría de teléfonos)
├── app-armeabi-v7a-release.apk  (32-bit ARM)
└── app-x86_64-release.apk       (Intel)
```

### Instalar APK en teléfono:

**Método 1: Desde PC con ADB**
```powershell
adb install build\app\outputs\flutter-apk\app-arm64-v8a-release.apk
```

**Método 2: Transferir archivo**
1. Envía el APK a tu teléfono (Google Drive, WhatsApp, USB, etc.)
2. Abre el archivo desde el teléfono
3. Permite "Instalar desde fuentes desconocidas"
4. Instala

---

## 🐛 PROBLEMAS COMUNES

### "flutter: command not found"
→ Flutter no está en el PATH. Cierra y abre nueva terminal después de agregarlo.

### "Unable to locate Android SDK"
→ Ejecuta: `flutter config --android-sdk C:\Users\TU_USUARIO\AppData\Local\Android\Sdk`

### "No connected devices"
→ Para emulador: `flutter emulators --launch <nombre>`
→ Para físico: Verifica depuración USB esté activada

### "Gradle build failed"
```powershell
cd android
.\gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### "SocketException: Failed host lookup"
→ Backend no está corriendo o URL incorrecta
→ Verifica: `http://10.0.2.2:8000` para emulador
→ O tu IP local para dispositivo físico

### App se cierra al abrir
```powershell
# Ver logs en tiempo real
flutter logs
# O desde ADB:
adb logcat | Select-String "flutter"
```

---

## 📞 ¿NECESITAS AYUDA?

1. **Revisa documentación completa**: `README.md`
2. **Guía rápida**: `QUICK_START.md`
3. **Detalles de implementación**: `IMPLEMENTACION_COMPLETA.md`
4. **Flutter oficial**: https://docs.flutter.dev/

---

## 🎯 RESULTADO ESPERADO

Al final de este checklist deberías tener:

- ✅ Flutter instalado y funcionando
- ✅ Android Studio configurado
- ✅ Emulador o dispositivo listo
- ✅ Backend corriendo en 0.0.0.0:8000
- ✅ App móvil ejecutándose
- ✅ Todas las funcionalidades probadas
- ✅ APK generado para distribución

**¡Buena suerte! 🚀**
