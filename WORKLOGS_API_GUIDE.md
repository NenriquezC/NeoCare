# 📚 Guía Completa de la API de Worklogs (Timesheets)

**NeoCare Health** — Sistema de Registro de Horas  
**Versión:** 1.0  
**Última actualización:** 13 de Enero 2026

---

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Modelo de Datos](#modelo-de-datos)
3. [Endpoints de la API](#endpoints-de-la-api)
4. [Validaciones y Reglas de Negocio](#validaciones-y-reglas-de-negocio)
5. [Permisos y Seguridad](#permisos-y-seguridad)
6. [Ejemplos con cURL](#ejemplos-con-curl)
7. [Ejemplos con Postman](#ejemplos-con-postman)
8. [Códigos de Error](#códigos-de-error)
9. [Casos Límite y Edge Cases](#casos-límite-y-edge-cases)
10. [Vista "Mis Horas"](#vista-mis-horas)

---

## 🎯 Descripción General

El módulo de **Worklogs** (Timesheets) permite a los usuarios registrar las horas trabajadas en tarjetas específicas del sistema Kanban de NeoCare.

**Características principales:**
- ✅ Registrar horas por tarjeta con fecha, cantidad de horas y nota opcional
- ✅ Editar y eliminar registros propios
- ✅ Ver listado de horas por tarjeta (todos los miembros del equipo)
- ✅ Ver resumen semanal personal ("Mis Horas")
- ✅ Validaciones cliente y servidor
- ✅ Control de acceso basado en permisos de tablero y propiedad de registros

---

## 📊 Modelo de Datos

### Tabla: `time_entries`

| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| `card_id` | INTEGER | NOT NULL, FK → cards(id) ON DELETE CASCADE | Tarjeta asociada |
| `user_id` | INTEGER | NOT NULL, FK → users(id) | Usuario que registró las horas |
| `date` | DATE | NOT NULL | Fecha del trabajo realizado |
| `hours` | NUMERIC(5,2) | NOT NULL | Horas trabajadas (máx 999.99) |
| `note` | TEXT | NULLABLE | Nota o descripción del trabajo |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación del registro |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | Última actualización |

**Relaciones:**
- Un `time_entry` pertenece a una `card`
- Un `time_entry` pertenece a un `user`
- Si se elimina una tarjeta, se eliminan todos sus `time_entries` (CASCADE)

---

## 🔌 Endpoints de la API

### 1. Crear Worklog

**Endpoint:** `POST /worklogs/`  
**Autenticación:** JWT requerido  
**Permisos:** Usuario debe ser miembro o propietario del tablero de la tarjeta

**Request Body:**
```json
{
  "card_id": 123,
  "date": "2026-01-13",
  "hours": 3.5,
  "note": "Implementación de validaciones"
}
```

**Response (201 Created):**
```json
{
  "id": 456,
  "card_id": 123,
  "user_id": 1,
  "date": "2026-01-13",
  "hours": "3.50",
  "note": "Implementación de validaciones",
  "created_at": "2026-01-13T10:30:00Z",
  "updated_at": "2026-01-13T10:30:00Z"
}
```

**Validaciones:**
- `card_id`: Debe existir y el usuario debe tener acceso al tablero
- `date`: No puede ser futura
- `hours`: Debe ser > 0 (se recomienda mínimo 0.25)
- `note`: Máximo 200 caracteres

---

### 2. Listar Worklogs por Tarjeta

**Endpoint:** `GET /worklogs/card/{card_id}`  
**Autenticación:** JWT requerido  
**Permisos:** Usuario debe ser miembro o propietario del tablero

**Response (200 OK):**
```json
[
  {
    "id": 456,
    "card_id": 123,
    "user_id": 1,
    "date": "2026-01-13",
    "hours": "3.50",
    "note": "Implementación de validaciones",
    "created_at": "2026-01-13T10:30:00Z",
    "updated_at": "2026-01-13T10:30:00Z"
  },
  {
    "id": 457,
    "card_id": 123,
    "user_id": 2,
    "date": "2026-01-12",
    "hours": "5.00",
    "note": "Revisión de código",
    "created_at": "2026-01-12T15:20:00Z",
    "updated_at": "2026-01-12T15:20:00Z"
  }
]
```

**Ordenamiento:** Descendente por fecha (más recientes primero)

---

### 3. Editar Worklog

**Endpoint:** `PATCH /worklogs/{worklog_id}`  
**Autenticación:** JWT requerido  
**Permisos:** Solo el autor del registro puede editarlo

**Request Body (todos los campos opcionales):**
```json
{
  "date": "2026-01-12",
  "hours": 4.0,
  "note": "Nota actualizada"
}
```

**Response (200 OK):**
```json
{
  "id": 456,
  "card_id": 123,
  "user_id": 1,
  "date": "2026-01-12",
  "hours": "4.00",
  "note": "Nota actualizada",
  "created_at": "2026-01-13T10:30:00Z",
  "updated_at": "2026-01-13T11:45:00Z"
}
```

**Validaciones:**
- `date` (si se proporciona): No puede ser futura
- `hours` (si se proporciona): Debe ser > 0
- `note` (si se proporciona): Máximo 200 caracteres

---

### 4. Eliminar Worklog

**Endpoint:** `DELETE /worklogs/{worklog_id}`  
**Autenticación:** JWT requerido  
**Permisos:** Solo el autor del registro puede eliminarlo

**Response (204 No Content):**
Sin cuerpo de respuesta

---

### 5. Mis Horas (Resumen Semanal)

**Endpoint:** `GET /worklogs/me/week?week=YYYY-WW`  
**Autenticación:** JWT requerido  
**Parámetros:**
- `week` (opcional): Semana en formato ISO `YYYY-WW` (ejemplo: `2026-02`). Si no se proporciona, usa la semana actual.

**Response (200 OK):**
```json
{
  "week": "2026-02",
  "total_hours": "12.50",
  "by_day": [
    {
      "date": "2026-01-13",
      "total_hours": "7.50"
    },
    {
      "date": "2026-01-12",
      "total_hours": "5.00"
    }
  ],
  "entries": [
    {
      "id": 456,
      "card_id": 123,
      "user_id": 1,
      "date": "2026-01-13",
      "hours": "3.50",
      "note": "Implementación de validaciones",
      "created_at": "2026-01-13T10:30:00Z",
      "updated_at": "2026-01-13T10:30:00Z"
    },
    {
      "id": 458,
      "card_id": 124,
      "user_id": 1,
      "date": "2026-01-13",
      "hours": "4.00",
      "note": "Testing E2E",
      "created_at": "2026-01-13T14:15:00Z",
      "updated_at": "2026-01-13T14:15:00Z"
    }
  ]
}
```

---

## ✅ Validaciones y Reglas de Negocio

### Validaciones del Cliente (Frontend)

1. **Horas mínimas:** 0.25 horas (15 minutos)
2. **Fecha:**
   - No puede estar vacía
   - No puede ser futura
   - Input HTML con `max` = fecha actual
3. **Nota:**
   - Opcional
   - Máximo 200 caracteres
   - Input HTML con `maxlength="200"`

### Validaciones del Servidor (Backend)

1. **Campo `card_id`:**
   - ✅ Requerido
   - ✅ Debe existir en la tabla `cards`
   - ✅ Usuario debe tener acceso al tablero de la tarjeta (miembro o propietario)

2. **Campo `date`:**
   - ✅ Requerido
   - ✅ Formato válido (`YYYY-MM-DD`)
   - ✅ No puede ser futura (validación: `date <= date.today()`)

3. **Campo `hours`:**
   - ✅ Requerido
   - ✅ Tipo: Decimal (hasta 5 dígitos, 2 decimales)
   - ✅ Debe ser > 0 (Pydantic Field con `gt=0`)

4. **Campo `note`:**
   - ✅ Opcional (puede ser `null`)
   - ✅ Máximo 200 caracteres (Pydantic Field con `max_length=200`)

---

## 🔐 Permisos y Seguridad

### Autenticación

**Todos los endpoints requieren JWT válido.**

**Headers necesarios:**
```
Authorization: Bearer <token>
```

**Sin token válido:**
- Status: `401 Unauthorized` o `403 Forbidden`

### Permisos por Endpoint

| Endpoint | Permiso Requerido |
|----------|-------------------|
| `POST /worklogs/` | Miembro o propietario del tablero de la tarjeta |
| `GET /worklogs/card/{card_id}` | Miembro o propietario del tablero |
| `PATCH /worklogs/{id}` | **Solo el autor** del worklog |
| `DELETE /worklogs/{id}` | **Solo el autor** del worklog |
| `GET /worklogs/me/week` | Usuario autenticado (solo ve sus propias horas) |

### Matriz de Permisos

| Acción | Propietario Tablero | Miembro Tablero | Autor Worklog | Otro Usuario |
|--------|---------------------|-----------------|---------------|--------------|
| Crear worklog en tarjeta | ✅ | ✅ | ✅ | ❌ |
| Ver worklogs de tarjeta | ✅ | ✅ | ✅ | ❌ |
| Editar worklog | ❌ | ❌ | ✅ Solo si es autor | ❌ |
| Eliminar worklog | ❌ | ❌ | ✅ Solo si es autor | ❌ |

**Nota importante:** Ni siquiera el propietario del tablero puede editar o eliminar worklogs de otros usuarios. Esto garantiza la integridad de los registros de tiempo.

---

## 🔧 Ejemplos con cURL

### 1. Crear Worklog

```bash
curl -X POST http://127.0.0.1:8000/worklogs/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": 123,
    "date": "2026-01-13",
    "hours": 3.5,
    "note": "Implementación de validaciones"
  }'
```

### 2. Listar Worklogs de una Tarjeta

```bash
curl -X GET http://127.0.0.1:8000/worklogs/card/123 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Editar Worklog

```bash
curl -X PATCH http://127.0.0.1:8000/worklogs/456 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hours": 4.0,
    "note": "Horas actualizadas"
  }'
```

### 4. Eliminar Worklog

```bash
curl -X DELETE http://127.0.0.1:8000/worklogs/456 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. Mis Horas (Semana Actual)

```bash
curl -X GET "http://127.0.0.1:8000/worklogs/me/week" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Mis Horas (Semana Específica)

```bash
curl -X GET "http://127.0.0.1:8000/worklogs/me/week?week=2026-02" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📮 Ejemplos con Postman

### Configuración Inicial

1. **Crear variable de entorno:**
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: (se llenará después del login)

2. **Login y obtención de token:**
   ```
   POST {{base_url}}/auth/login
   Body (JSON):
   {
     "email": "tu@email.com",
     "password": "tu_password"
   }
   
   En Tests, agregar:
   pm.environment.set("token", pm.response.json().access_token);
   ```

3. **Configurar Authorization en todos los requests:**
   - Type: `Bearer Token`
   - Token: `{{token}}`

### Collection de Requests

#### 1. Crear Worklog
```
POST {{base_url}}/worklogs/
Headers: Authorization: Bearer {{token}}
Body (JSON):
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 2.5,
  "note": "Desarrollo de features"
}
```

#### 2. Listar Worklogs de Tarjeta
```
GET {{base_url}}/worklogs/card/1
Headers: Authorization: Bearer {{token}}
```

#### 3. Editar Worklog
```
PATCH {{base_url}}/worklogs/1
Headers: Authorization: Bearer {{token}}
Body (JSON):
{
  "hours": 3.0,
  "note": "Actualizado desde Postman"
}
```

#### 4. Eliminar Worklog
```
DELETE {{base_url}}/worklogs/1
Headers: Authorization: Bearer {{token}}
```

#### 5. Mis Horas (Semana Actual)
```
GET {{base_url}}/worklogs/me/week
Headers: Authorization: Bearer {{token}}
```

### Tests Automatizados en Postman

**Para crear worklog:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Worklog created with correct hours", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.hours).to.eql("2.50");
});

// Guardar worklog_id para usar en otros requests
pm.environment.set("worklog_id", pm.response.json().id);
```

**Para validar fecha futura (debe fallar):**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error message mentions future date", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include("futuras");
});
```

---

## ⚠️ Códigos de Error

| Código | Descripción | Causa Común |
|--------|-------------|-------------|
| `200` | OK | Request exitoso (GET, PATCH) |
| `201` | Created | Worklog creado exitosamente |
| `204` | No Content | Worklog eliminado exitosamente |
| `400` | Bad Request | Fecha futura, formato inválido |
| `401` | Unauthorized | Token JWT faltante o inválido |
| `403` | Forbidden | Acceso denegado (no es autor o no es miembro del tablero) |
| `404` | Not Found | Worklog o tarjeta no encontrada |
| `422` | Unprocessable Entity | Validación Pydantic fallida (hours <= 0, note > 200 chars) |
| `500` | Internal Server Error | Error del servidor |

### Ejemplos de Respuestas de Error

**400 - Fecha futura:**
```json
{
  "detail": "No se pueden registrar horas en fechas futuras"
}
```

**403 - No es autor:**
```json
{
  "detail": "No autorizado"
}
```

**403 - No es miembro del tablero:**
```json
{
  "detail": "No tienes acceso a esta tarjeta"
}
```

**404 - Worklog no encontrado:**
```json
{
  "detail": "Registro no encontrado"
}
```

**422 - Validación Pydantic (hours = 0):**
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "hours"],
      "msg": "Input should be greater than 0",
      "input": 0,
      "ctx": {"gt": 0}
    }
  ]
}
```

**422 - Validación Pydantic (note > 200 chars):**
```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "note"],
      "msg": "String should have at most 200 characters",
      "input": "...",
      "ctx": {"max_length": 200}
    }
  ]
}
```

---

## 🧪 Casos Límite y Edge Cases

### 1. Horas = 0.01 (mínimo técnico)

**Comportamiento:** ✅ Permitido por backend (gt=0), pero frontend recomienda mínimo 0.25

```json
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 0.01,
  "note": "Horas mínimas"
}
```

**Response:** 201 Created (válido)

### 2. Fecha = Hoy

**Comportamiento:** ✅ Permitido

```json
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 2.0
}
```

### 3. Fecha = Mañana

**Comportamiento:** ❌ Rechazado

```json
{
  "card_id": 1,
  "date": "2026-01-14",
  "hours": 2.0
}
```

**Response:** 400 Bad Request

### 4. Nota = null vs ""

**Comportamiento:** Ambos son válidos y se almacenan como `null`

```json
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 2.0,
  "note": null
}
```

```json
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 2.0,
  "note": ""
}
```

Ambos almacenan `note` como `null` en BD.

### 5. Múltiples Worklogs en la Misma Tarjeta

**Comportamiento:** ✅ Permitido (no hay constraint de unicidad)

Un usuario puede registrar múltiples worklogs en la misma tarjeta en diferentes fechas, o incluso en la misma fecha.

### 6. Editar Solo un Campo

**Comportamiento:** ✅ PATCH permite actualización parcial

```json
{
  "hours": 5.0
}
```

Solo actualiza `hours`, dejando `date` y `note` sin cambios.

### 7. Eliminar Tarjeta con Worklogs

**Comportamiento:** ✅ CASCADE DELETE elimina automáticamente todos los worklogs asociados

No se requiere acción manual.

### 8. Usuario Removido del Tablero

**Comportamiento:** 
- ✅ Los worklogs existentes persisten (no se eliminan)
- ❌ El usuario ya no puede ver, editar o crear nuevos worklogs en tarjetas de ese tablero

### 9. Horas Máximas (999.99)

**Comportamiento:** ✅ Permitido por el tipo NUMERIC(5,2)

```json
{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 999.99
}
```

### 10. Formato de Semana Incorrecto

**Request:** `GET /worklogs/me/week?week=2026-W02` (con "W")

**Comportamiento:** ❌ Rechazado

**Response:** 400 Bad Request
```json
{
  "detail": "Formato de semana inválido (usa YYYY-WW, ejemplo: 2026-03)"
}
```

**Formato correcto:** `2026-02` (sin "W")

---

## 📊 Vista "Mis Horas"

### Descripción

La vista **"Mis Horas"** es una pantalla en el frontend que muestra el resumen de horas trabajadas por el usuario actual en una semana específica.

### Ubicación en el Frontend

- **Ruta:** `/my-hours`
- **Acceso:** Menú principal (navegación protegida)
- **Componente:** `frontend_t/src/pages/MyHours.tsx`

### Funcionalidades

1. **Selector de Semana:**
   - Por defecto muestra la semana actual
   - Permite navegar a semanas anteriores/posteriores

2. **Resumen por Día:**
   - Listado de fechas con total de horas por día
   - Ordenado cronológicamente

3. **Total Semanal:**
   - Suma de todas las horas de la semana
   - Destacado visualmente

4. **Listado Detallado:**
   - Todos los registros individuales de la semana
   - Incluye: fecha, horas, nota, tarjeta asociada
   - Permite ver contexto completo

5. **Formulario de Registro Rápido (Opcional):**
   - Algunos frontends incluyen formulario para añadir horas directamente desde esta vista
   - Requiere seleccionar tablero y tarjeta

### Ejemplo Visual (Pseudo-código)

```
┌─────────────────────────────────────────┐
│  Mis Horas - Semana 2026-02             │
│  [<] Semana 2026-02 [>]                 │
├─────────────────────────────────────────┤
│  📊 Total Semanal: 12.50 horas          │
├─────────────────────────────────────────┤
│  Por Día:                               │
│  ✓ 13/01/2026: 7.50h                    │
│  ✓ 12/01/2026: 5.00h                    │
├─────────────────────────────────────────┤
│  Detalle de Registros:                  │
│  ┌───────────────────────────────────┐  │
│  │ 13/01 - 3.50h - Tarjeta #123     │  │
│  │ "Implementación de validaciones" │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ 13/01 - 4.00h - Tarjeta #124     │  │
│  │ "Testing E2E"                     │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Endpoint Consumido

```
GET /worklogs/me/week?week=YYYY-WW
```

**Response usado para renderizar:**
```json
{
  "week": "2026-02",
  "total_hours": "12.50",          // → Total Semanal
  "by_day": [                      // → Resumen por Día
    {
      "date": "2026-01-13",
      "total_hours": "7.50"
    },
    {
      "date": "2026-01-12",
      "total_hours": "5.00"
    }
  ],
  "entries": [                     // → Listado Detallado
    {
      "id": 456,
      "card_id": 123,
      "date": "2026-01-13",
      "hours": "3.50",
      "note": "Implementación de validaciones"
    },
    {
      "id": 458,
      "card_id": 124,
      "date": "2026-01-13",
      "hours": "4.00",
      "note": "Testing E2E"
    }
  ]
}
```

---

## 🧪 Cómo Testear Manualmente

### Flujo Completo de Prueba

1. **Preparación:**
   - Registrar/login de usuario
   - Crear un tablero
   - Crear una tarjeta en el tablero

2. **Crear Worklog:**
   - POST `/worklogs/` con `card_id`, `date`, `hours`, `note`
   - Verificar status 201
   - Guardar `id` del worklog creado

3. **Listar Worklogs:**
   - GET `/worklogs/card/{card_id}`
   - Verificar que aparece el worklog creado

4. **Editar Worklog:**
   - PATCH `/worklogs/{id}` con nuevos valores
   - Verificar status 200
   - Listar de nuevo para confirmar cambios

5. **Ver en "Mis Horas":**
   - GET `/worklogs/me/week` (semana actual)
   - Verificar que el total incluye el worklog

6. **Eliminar Worklog:**
   - DELETE `/worklogs/{id}`
   - Verificar status 204
   - Listar de nuevo para confirmar eliminación

### Casos de Error a Probar

1. **Sin token:**
   - Cualquier endpoint sin header `Authorization`
   - Debe retornar 401 o 403

2. **Fecha futura:**
   - POST con `date` > hoy
   - Debe retornar 400

3. **Hours = 0:**
   - POST con `hours: 0`
   - Debe retornar 422

4. **Nota > 200 chars:**
   - POST con `note` de 201+ caracteres
   - Debe retornar 422

5. **Editar worklog ajeno:**
   - Crear worklog con usuario A
   - Login como usuario B
   - Intentar PATCH del worklog de A
   - Debe retornar 403

6. **Tarjeta de otro tablero:**
   - Usuario A no es miembro del tablero X
   - Intentar POST worklog en tarjeta del tablero X
   - Debe retornar 403

---

## 📝 Notas Finales

### Diferencias con Documentación Original (README_Semana_4.md)

1. **Endpoints:**
   - Docs originales: `POST /cards/{card_id}/worklogs`
   - Implementación real: `POST /worklogs/` (con `card_id` en body)
   - **Razón:** Mejor alineación con estándares REST y reducción de redundancia

2. **Método de Actualización:**
   - Docs originales: `PATCH /worklogs/{id}`
   - Implementación inicial: `PUT /worklogs/{id}`
   - **Actualización (13 Ene 2026):** ✅ Cambiado a `PATCH` según estándar REST

3. **Formato de Semana:**
   - Docs: `YYYY-WW` (sin letra "W" intermedia)
   - Implementación: `YYYY-WW` (ejemplo: `2026-02`)
   - **Nota:** Backend acepta formato sin "W" intermedia

### Recomendaciones

- ✅ Usar siempre `PATCH` para actualizaciones parciales
- ✅ Validar en cliente antes de enviar al servidor (mejor UX)
- ✅ Implementar debouncing en inputs de horas para evitar requests excesivos
- ✅ Mostrar mensajes de error claros al usuario
- ✅ Usar formato de fecha ISO (`YYYY-MM-DD`) consistentemente
- ✅ Implementar loading states en operaciones asíncronas

### Recursos Adicionales

- **Swagger UI:** `http://127.0.0.1:8000/docs` (cuando backend está corriendo)
- **Postman Collection:** `NeoCare_Postman_Collection_Updated.json`
- **Tests Automatizados:** `backend/tests/worklogs/test_worklogs.py`
- **Tests E2E:** `backend/tests/e2e/test_e2e.py` → `test_e2e_worklogs_complete_flow`

---

**Versión del Documento:** 1.0  
**Autor:** Equipo NeoCare  
**Última Revisión:** 13 de Enero 2026

