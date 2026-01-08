# Scripts de Gestión del Backend NeoCare

Esta carpeta contiene scripts de utilidad para configuración y validación del backend.

## 📋 Scripts Disponibles

### 🔥 Gestión de Firewall

#### `setup-firewall.ps1`
**Propósito:** Configurar reglas de firewall para permitir conexiones desde la app móvil.

**Uso:**
```powershell
# Ejecutar como Administrador
.\setup-firewall.ps1
```

**Qué hace:**
- Crea regla para puerto TCP 8000 (todos los perfiles de red)
- Crea regla para la aplicación Python del backend
- Permite conexiones entrantes desde dispositivos en la red local

**Cuándo usar:**
- Primera configuración del proyecto
- Después de reinstalar Windows o resetear firewall
- Si la app móvil no puede conectarse al backend

---

#### `change-network-to-private.ps1`
**Propósito:** Cambiar el perfil de red WiFi de Público a Privado.

**Uso:**
```powershell
# Ejecutar como Administrador
.\change-network-to-private.ps1
```

**Qué hace:**
- Verifica el perfil actual de la red WiFi
- Cambia de "Público" a "Privado" si es necesario
- Permite que las reglas de firewall funcionen correctamente

**Cuándo usar:**
- Si la app móvil no conecta a pesar de tener las reglas de firewall
- Si tu red doméstica está configurada como Pública por error
- Para desarrollo local (solo en redes confiables)

**⚠️ Nota:** Solo usa este script en tu red doméstica o redes confiables.

---

### 🧪 Validación y Testing

#### `test_connectivity.py`
**Propósito:** Validar la conectividad entre el backend y la app móvil.

**Uso:**
```bash
python test_connectivity.py
```

**Qué hace:**
- Simula una petición de login desde la app móvil
- Verifica que el backend responde correctamente
- Muestra información detallada de errores si falla

**Cuándo usar:**
- Antes de probar con la app móvil
- Para diagnosticar problemas de conectividad
- Después de cambiar configuración de red o firewall

**Salida esperada:**
```
✓✓ LOGIN EXITOSO ✓✓
  Token recibido: eyJhbGci...
  Token Type: bearer
```

---

#### `create_mobile_user.py`
**Propósito:** Crear o actualizar el usuario de prueba para la app móvil.

**Uso:**
```bash
python create_mobile_user.py
```

**Qué hace:**
- Crea el usuario `movil@test.com` con contraseña `123456`
- Si ya existe, actualiza la contraseña
- Configura el hash de contraseña correctamente

**Cuándo usar:**
- Primera configuración del proyecto
- Si olvidaste las credenciales de prueba
- Si necesitas resetear la contraseña del usuario móvil

**Credenciales creadas:**
- **Email:** movil@test.com
- **Password:** 123456

---

## 🚀 Flujo de Configuración Completo

### Primera vez configurando el proyecto:

1. **Crear usuario de prueba:**
   ```bash
   python create_mobile_user.py
   ```

2. **Configurar firewall (como Administrador):**
   ```powershell
   .\setup-firewall.ps1
   ```

3. **Si la red es Pública, cambiar a Privada (como Administrador):**
   ```powershell
   .\change-network-to-private.ps1
   ```

4. **Validar conectividad:**
   ```bash
   python test_connectivity.py
   ```

5. **Usar en la app móvil:**
   - URL: `http://192.168.1.39:8000`
   - Email: `movil@test.com`
   - Password: `123456`

---

## 🔍 Solución de Problemas

### La app móvil no conecta

**Paso 1:** Verificar conectividad desde la PC
```bash
python test_connectivity.py
```

**Si falla:**
- ✅ Verificar que el backend esté corriendo
- ✅ Verificar la IP de la PC (debe ser 192.168.1.39)

**Si funciona en PC pero no en móvil:**
1. Verificar que el móvil esté en la misma red WiFi
2. Ejecutar `setup-firewall.ps1` como Administrador
3. Verificar perfil de red y ejecutar `change-network-to-private.ps1` si es necesario

---

### Error "Connection refused" o "Timeout"

**Causa:** Firewall bloqueando conexiones

**Solución:**
```powershell
# Como Administrador
.\setup-firewall.ps1
```

---

### Error "Credenciales incorrectas"

**Causa:** Usuario no existe o contraseña incorrecta

**Solución:**
```bash
python create_mobile_user.py
```

Usa las credenciales:
- Email: `movil@test.com`
- Password: `123456`

---

## 📝 Notas Importantes

- **Todos los scripts PowerShell (.ps1) requieren permisos de Administrador**
- **Los scripts Python deben ejecutarse desde el directorio `backend`**
- **La IP 192.168.1.39 debe coincidir con la IP actual de tu PC**
- **El backend debe estar corriendo en el puerto 8000**
- **El móvil debe estar en la misma red WiFi que la PC**

---

## 🔐 Perfiles de Red en Windows

### Red Privada (Private)
- ✅ Usar en redes domésticas y confiables
- ✅ Permite compartir archivos
- ✅ Permite conexiones entrantes (desarrollo)

### Red Pública (Public)
- 🔒 Usar en cafeterías, aeropuertos, hoteles
- 🔒 Bloquea conexiones entrantes
- 🔒 Mayor seguridad

**Para desarrollo:** Usa siempre perfil Privado en tu red doméstica.
