# Configuración de Git en IntelliJ IDEA

## ✅ Configuración de Git completada (vía terminal)

Se ha configurado Git globalmente con los siguientes valores:

- **Usuario**: `raquelmartinesbec-glitch`
- **Email**: `raquelmartinesbec-glitch@users.noreply.github.com`
- **Credential Helper**: `manager` (Git Credential Manager)
- **Repositorio remoto**: `https://github.com/NenriquezC/NeoCare.git`

---

## 🔧 Pasos para configurar la autenticación en IntelliJ IDEA

### 1. Verificar la integración de Git en IntelliJ

1. Abre **IntelliJ IDEA**
2. Ve a **File > Settings** (o presiona `Ctrl + Alt + S`)
3. Navega a **Version Control > Git**
4. Verifica que la ruta del ejecutable de Git esté configurada:
   - Debería apuntar a: `C:\Program Files\Git\bin\git.exe` (o similar)
   - Haz clic en **Test** para verificar que funciona

### 2. Configurar la autenticación con GitHub

IntelliJ IDEA soporta dos métodos principales:

#### **Opción A: Token de Acceso Personal (RECOMENDADO)**

1. Ve a **File > Settings > Version Control > GitHub**
2. Haz clic en el botón **+** (Add Account)
3. Selecciona **"Log In with Token..."**
4. Genera un token en GitHub:
   - Visita: https://github.com/settings/tokens
   - Haz clic en **Generate new token (classic)**
   - Selecciona los scopes necesarios:
     - ✅ `repo` (acceso completo a repositorios privados)
     - ✅ `workflow` (si usas GitHub Actions)
   - Copia el token generado
5. Pega el token en IntelliJ y haz clic en **Add Account**

#### **Opción B: Usar Git Credential Manager (Ya configurado)**

Git Credential Manager ya está configurado globalmente. Al hacer tu primera operación Git (pull, push, fetch) desde IntelliJ:

1. IntelliJ usará automáticamente Git Credential Manager
2. Se abrirá una ventana del navegador para autenticarte con GitHub
3. Las credenciales se guardarán automáticamente en Windows Credential Manager

### 3. Probar la conexión

1. En IntelliJ, ve a **VCS > Git > Fetch** (o presiona `Ctrl + T`)
2. Si se te solicita autenticación:
   - **Si usaste Token**: Ya debería estar configurado
   - **Si usas Credential Manager**: Se abrirá el navegador para autenticarte
3. Una vez autenticado, las credenciales se guardarán para futuros usos

### 4. Verificar que funciona

Ejecuta cualquiera de estas operaciones desde IntelliJ:
- **VCS > Git > Pull** - Descargar cambios
- **VCS > Git > Push** - Subir cambios
- **VCS > Git > Fetch** - Actualizar referencias

---

## 🔑 Gestión de Credenciales en Windows

Las credenciales se almacenan en **Windows Credential Manager**:

1. Presiona `Win + R`
2. Escribe: `control /name Microsoft.CredentialManager`
3. Ve a **Credenciales de Windows > Credenciales genéricas**
4. Busca entradas de `git:https://github.com`

Si necesitas eliminar o actualizar credenciales, hazlo desde aquí.

---

## 🚀 Comandos Git útiles desde la terminal (ya configurados)

```bash
# Ver configuración actual
git config --list --global

# Hacer pull
git pull origin main

# Hacer push
git push origin main

# Ver estado
git status

# Ver ramas
git branch -a
```

---

## ✅ Estado Actual

- ✅ Git configurado globalmente
- ✅ Usuario y email configurados
- ✅ Credential Helper configurado (Windows Credential Manager)
- ✅ Repositorio remoto configurado con HTTPS
- ⏳ Pendiente: Configurar cuenta de GitHub en IntelliJ IDEA (sigue los pasos de arriba)

---

## 📝 Notas

- IntelliJ IDEA detecta automáticamente la configuración global de Git
- No necesitas configurar usuario/email dentro de IntelliJ, ya está global
- El primer `push` o `pull` solicitará autenticación (solo una vez)
- Las credenciales se almacenan de forma segura en Windows

---

**Fecha de configuración**: 2026-01-14

