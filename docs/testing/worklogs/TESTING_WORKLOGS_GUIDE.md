# 🧪 Guía de Testing - Módulo Worklogs

**NeoCare Health** — Instrucciones para Ejecutar Tests  
**Última actualización:** 13 de Enero 2026

---

## 📋 Índice

1. [Configuración del Entorno](#configuración-del-entorno)
2. [Tests Unitarios](#tests-unitarios)
3. [Tests End-to-End (E2E)](#tests-end-to-end-e2e)
4. [Pruebas Manuales con Postman](#pruebas-manuales-con-postman)
5. [Verificación Rápida del Flujo](#verificación-rápida-del-flujo)

---

## ⚙️ Configuración del Entorno

### Prerequisitos

1. **Python 3.12+** instalado
2. **Node.js 18+** (para frontend)
3. **PostgreSQL** corriendo (para backend)
4. **Git** para clonar el repositorio

### Instalación de Dependencias

#### Backend

```powershell
# Desde la raíz del proyecto
cd NeoCare

# Activar entorno virtual (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Navegar a backend
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación de pytest
python -m pytest --version
```

#### Frontend

```powershell
# Desde la raíz del proyecto
cd NeoCare\frontend_t

# Instalar dependencias
npm install
```

### Configuración de Base de Datos

```powershell
# En backend, crear base de datos de testing
# Editar .env o usar variables de entorno

# Ejecutar migraciones
cd backend
alembic upgrade head
```

---

## 🧪 Tests Unitarios

### Ejecutar Todos los Tests de Worklogs

```powershell
# Activar entorno virtual
cd C:\Desarrollo\github\NeoCare
.\.venv\Scripts\Activate.ps1

# Navegar a backend
cd backend

# Ejecutar tests de worklogs con verbose
python -m pytest tests/worklogs/test_worklogs.py -v

# Ejecutar con cobertura
python -m pytest tests/worklogs/test_worklogs.py --cov=app.worklogs --cov-report=html
```

### Salida Esperada

```
tests/worklogs/test_worklogs.py::test_create_worklog_success PASSED           [  7%]
tests/worklogs/test_worklogs.py::test_create_worklog_invalid_hours PASSED     [ 14%]
tests/worklogs/test_worklogs.py::test_create_worklog_future_date PASSED       [ 21%]
tests/worklogs/test_worklogs.py::test_list_worklogs PASSED                    [ 28%]
tests/worklogs/test_worklogs.py::test_update_worklog_own PASSED               [ 35%]
tests/worklogs/test_worklogs.py::test_update_worklog_other_user PASSED        [ 42%]
tests/worklogs/test_worklogs.py::test_delete_worklog_own PASSED               [ 50%]
tests/worklogs/test_worklogs.py::test_my_hours_week PASSED                    [ 57%]
tests/worklogs/test_worklogs.py::test_delete_worklog_other_user PASSED        [ 64%]
tests/worklogs/test_worklogs.py::test_create_worklog_without_token PASSED     [ 71%]
tests/worklogs/test_worklogs.py::test_list_worklogs_without_token PASSED      [ 78%]
tests/worklogs/test_worklogs.py::test_update_worklog_without_token PASSED     [ 85%]
tests/worklogs/test_worklogs.py::test_delete_worklog_without_token PASSED     [ 92%]

========================== 13 passed in 5.23s ==========================
```

### Tests Disponibles

| Test | Descripción |
|------|-------------|
| `test_create_worklog_success` | Crear worklog válido |
| `test_create_worklog_invalid_hours` | Rechazar hours=0 (422) |
| `test_create_worklog_future_date` | Rechazar fecha futura (400) |
| `test_list_worklogs` | Listar worklogs de tarjeta |
| `test_update_worklog_own` | Editar worklog propio |
| `test_update_worklog_other_user` | No permitir editar worklogs ajenos (403) |
| `test_delete_worklog_own` | Eliminar worklog propio |
| `test_delete_worklog_other_user` | No permitir eliminar worklogs ajenos (403) |
| `test_my_hours_week` | Ver resumen semanal |
| `test_create_worklog_without_token` | Crear sin auth (401/403) |
| `test_list_worklogs_without_token` | Listar sin auth (401/403) |
| `test_update_worklog_without_token` | Editar sin auth (401/403) |
| `test_delete_worklog_without_token` | Eliminar sin auth (401/403) |

### Ejecutar un Test Específico

```powershell
# Un solo test
python -m pytest tests/worklogs/test_worklogs.py::test_create_worklog_success -v

# Tests de seguridad solamente
python -m pytest tests/worklogs/test_worklogs.py -k "without_token or other_user" -v
```

---

## 🌐 Tests End-to-End (E2E)

### Ejecutar Test E2E de Worklogs

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Asegurarse de que backend y frontend estén corriendo
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend_t
npm run dev

# Terminal 3: Tests E2E
cd backend
python -m pytest tests/e2e/test_e2e.py::test_e2e_worklogs_complete_flow -v -s
```

### Flujo del Test E2E

El test `test_e2e_worklogs_complete_flow` ejecuta:

1. ✅ Crear tarjeta
2. ✅ Añadir registro de horas (POST /worklogs/)
3. ✅ Listar horas de la tarjeta (GET /worklogs/card/{id})
4. ✅ Editar horas (PATCH /worklogs/{id})
5. ✅ Ver en "Mis Horas" semana actual (GET /worklogs/me/week)
6. ✅ Eliminar registro (DELETE /worklogs/{id})
7. ✅ Verificar eliminación

### Salida Esperada

```
📝 Paso 1: Crear tarjeta para worklog...
✅ Tarjeta creada: ID=123

⏱️ Paso 2: Añadir registro de horas...
✅ Worklog creado: ID=456, Horas=3.50

📋 Paso 3: Listar worklogs de la tarjeta...
✅ Worklogs listados: 1 registro(s)

✏️ Paso 4: Editar registro de horas...
✅ Worklog actualizado: Horas=5.00

📊 Paso 5: Verificar en 'Mis Horas' (semana actual)...
✅ Mis horas verificadas: Semana=2026-02, Total=5.0h

🗑️ Paso 6: Eliminar registro de horas...
✅ Worklog eliminado: ID=456

🔍 Paso 7: Verificar eliminación...
✅ Worklog eliminado correctamente

🎉 Flujo E2E de Worklogs completado exitosamente!
PASSED
```

---

## 📮 Pruebas Manuales con Postman

### Importar Collection

1. Abrir Postman
2. Importar archivo: `NeoCare_Postman_Collection_Updated.json`
3. Configurar variables de entorno:
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: (se llenará automáticamente al hacer login)

### Flujo de Prueba Manual

#### 1. Login

```
POST {{base_url}}/auth/login
Body:
{
  "email": "test@example.com",
  "password": "password123"
}

En "Tests", agregar:
pm.environment.set("token", pm.response.json().access_token);
```

#### 2. Crear Tablero y Tarjeta

```
POST {{base_url}}/boards/
Headers: Authorization: Bearer {{token}}
Body:
{
  "name": "Tablero de Pruebas"
}

Guardar board_id en variable de entorno
```

```
POST {{base_url}}/cards/
Headers: Authorization: Bearer {{token}}
Body:
{
  "title": "Tarjeta de Testing",
  "board_id": {{board_id}},
  "list_id": {{list_id}}
}

Guardar card_id en variable de entorno
```

#### 3. Tests de Worklogs

**Crear Worklog:**
```
POST {{base_url}}/worklogs/
Headers: Authorization: Bearer {{token}}
Body:
{
  "card_id": {{card_id}},
  "date": "2026-01-13",
  "hours": 3.5,
  "note": "Desarrollo de features"
}

En "Tests":
pm.test("Status 201", () => pm.response.to.have.status(201));
pm.environment.set("worklog_id", pm.response.json().id);
```

**Listar Worklogs:**
```
GET {{base_url}}/worklogs/card/{{card_id}}
Headers: Authorization: Bearer {{token}}

En "Tests":
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Array not empty", () => pm.expect(pm.response.json().length).to.be.above(0));
```

**Editar Worklog:**
```
PATCH {{base_url}}/worklogs/{{worklog_id}}
Headers: Authorization: Bearer {{token}}
Body:
{
  "hours": 5.0,
  "note": "Horas actualizadas"
}

En "Tests":
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Hours updated", () => pm.expect(pm.response.json().hours).to.eql("5.00"));
```

**Mis Horas:**
```
GET {{base_url}}/worklogs/me/week
Headers: Authorization: Bearer {{token}}

En "Tests":
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Has total_hours", () => pm.expect(pm.response.json()).to.have.property("total_hours"));
```

**Eliminar Worklog:**
```
DELETE {{base_url}}/worklogs/{{worklog_id}}
Headers: Authorization: Bearer {{token}}

En "Tests":
pm.test("Status 204", () => pm.response.to.have.status(204));
```

### Tests de Validación y Seguridad

**Fecha Futura (debe fallar):**
```
POST {{base_url}}/worklogs/
Headers: Authorization: Bearer {{token}}
Body:
{
  "card_id": {{card_id}},
  "date": "2027-01-01",
  "hours": 2.0
}

En "Tests":
pm.test("Status 400", () => pm.response.to.have.status(400));
pm.test("Error message", () => pm.expect(pm.response.json().detail).to.include("futuras"));
```

**Hours = 0 (debe fallar):**
```
POST {{base_url}}/worklogs/
Headers: Authorization: Bearer {{token}}
Body:
{
  "card_id": {{card_id}},
  "date": "2026-01-13",
  "hours": 0
}

En "Tests":
pm.test("Status 422", () => pm.response.to.have.status(422));
```

**Sin Token (debe fallar):**
```
GET {{base_url}}/worklogs/card/{{card_id}}
(Sin header Authorization)

En "Tests":
pm.test("Status 401 or 403", () => pm.expect([401, 403]).to.include(pm.response.code));
```

---

## ⚡ Verificación Rápida del Flujo

### Script PowerShell Automatizado

Crea un archivo `test-worklogs-quick.ps1`:

```powershell
# Quick test script para worklogs
$baseUrl = "http://127.0.0.1:8000"

Write-Host "🔐 Paso 1: Login..." -ForegroundColor Cyan
$loginBody = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access_token
Write-Host "✅ Token obtenido" -ForegroundColor Green

Write-Host "`n📝 Paso 2: Crear worklog..." -ForegroundColor Cyan
$worklogBody = @{
    card_id = 1
    date = (Get-Date -Format "yyyy-MM-dd")
    hours = 2.5
    note = "Test rápido"
} | ConvertTo-Json

$headers = @{
    Authorization = "Bearer $token"
}

$worklogResponse = Invoke-RestMethod -Uri "$baseUrl/worklogs/" -Method POST -Body $worklogBody -ContentType "application/json" -Headers $headers
$worklogId = $worklogResponse.id
Write-Host "✅ Worklog creado: ID=$worklogId" -ForegroundColor Green

Write-Host "`n📋 Paso 3: Listar worklogs..." -ForegroundColor Cyan
$listResponse = Invoke-RestMethod -Uri "$baseUrl/worklogs/card/1" -Method GET -Headers $headers
Write-Host "✅ Encontrados: $($listResponse.Count) worklogs" -ForegroundColor Green

Write-Host "`n📊 Paso 4: Ver mis horas..." -ForegroundColor Cyan
$myHoursResponse = Invoke-RestMethod -Uri "$baseUrl/worklogs/me/week" -Method GET -Headers $headers
Write-Host "✅ Total semanal: $($myHoursResponse.total_hours) horas" -ForegroundColor Green

Write-Host "`n🗑️ Paso 5: Eliminar worklog..." -ForegroundColor Cyan
Invoke-RestMethod -Uri "$baseUrl/worklogs/$worklogId" -Method DELETE -Headers $headers
Write-Host "✅ Worklog eliminado" -ForegroundColor Green

Write-Host "`n🎉 Verificación rápida completada!" -ForegroundColor Magenta
```

Ejecutar:
```powershell
.\test-worklogs-quick.ps1
```

---

## 🐛 Troubleshooting

### Error: "No module named pytest"

**Solución:**
```powershell
# Activar entorno virtual primero
.\.venv\Scripts\Activate.ps1
pip install pytest pytest-cov
```

### Error: "Database connection failed"

**Solución:**
1. Verificar que PostgreSQL está corriendo
2. Revisar credenciales en `.env`
3. Crear base de datos de testing si no existe

### Error: "401 Unauthorized" en tests

**Solución:**
1. Verificar que el token es válido
2. Revisar tiempo de expiración del JWT
3. Hacer login nuevamente

### Tests fallan con "No Python interpreter"

**Solución:**
- Esto es un warning del IDE, no afecta ejecución
- Configurar intérprete en IDE si molesta
- Los tests se ejecutan correctamente desde terminal

---

## 📊 Cobertura de Tests

### Generar Reporte de Cobertura

```powershell
cd backend
python -m pytest tests/worklogs/ --cov=app.worklogs --cov-report=html --cov-report=term
```

### Ver Reporte HTML

```powershell
# Abrir en navegador
start htmlcov/index.html
```

### Cobertura Esperada

- **Rutas:** ≥ 95%
- **Schemas:** 100%
- **Validaciones:** 100%

---

## 📝 Checklist de Pruebas Manuales

### Funcionalidad Básica
- [ ] Crear worklog válido
- [ ] Editar worklog propio
- [ ] Eliminar worklog propio
- [ ] Listar worklogs de tarjeta
- [ ] Ver "Mis Horas" semana actual

### Validaciones
- [ ] Rechazar hours = 0
- [ ] Rechazar fecha futura
- [ ] Rechazar nota > 200 chars
- [ ] Aceptar note = null

### Seguridad
- [ ] No permitir crear sin token
- [ ] No permitir editar worklog ajeno
- [ ] No permitir eliminar worklog ajeno
- [ ] No permitir acceso a tarjeta de otro tablero

### Edge Cases
- [ ] Múltiples worklogs misma tarjeta
- [ ] Worklog con hours mínimas (0.01)
- [ ] Eliminar tarjeta elimina sus worklogs
- [ ] Semana sin registros retorna vacío

---

**Última actualización:** 13 de Enero 2026  
**Mantenido por:** Equipo NeoCare

