# 📊 GUÍA COMPLETA DEL MÓDULO INFORME SEMANAL

**NeoCare Health** — Sistema de Reportes Kanban  
**Versión:** 1.0  
**Última actualización:** 13 de Enero 2026

---

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Arquitectura del Módulo](#arquitectura-del-módulo)
3. [Backend - API Endpoints](#backend---api-endpoints)
4. [Cálculo de Semana ISO](#cálculo-de-semana-iso)
5. [Consultas SQL Utilizadas](#consultas-sql-utilizadas)
6. [Frontend - Componentes](#frontend---componentes)
7. [Seguridad y Permisos](#seguridad-y-permisos)
8. [Casos Límite](#casos-límite)
9. [Optimización y Performance](#optimización-y-performance)
10. [Testing](#testing)
11. [Guía de Prueba Manual](#guía-de-prueba-manual)

---

## 🎯 Descripción General

El módulo de **Informe Semanal** permite a los usuarios visualizar métricas y estadísticas de productividad de sus tableros Kanban durante una semana específica.

**Funcionalidades principales:**
- ✅ Resumen de tareas (completadas, nuevas, vencidas)
- ✅ Horas trabajadas por usuario
- ✅ Horas trabajadas por tarjeta
- ✅ Exportación a CSV
- ✅ Filtrado por semana ISO
- ✅ Control de acceso basado en permisos de tablero

---

## 🏗️ Arquitectura del Módulo

### Backend (FastAPI)

```
backend/app/report/
├── routes.py       # Endpoints HTTP
├── services.py     # Lógica de negocio
└── schemas.py      # Modelos Pydantic
```

### Frontend (React + TypeScript)

```
frontend_t/src/
├── pages/
│   └── ReportPage.tsx                    # Vista principal
├── components/report/
│   ├── SummaryCards.tsx                  # Tarjetas de resumen
│   ├── HoursByUserTable.tsx              # Tabla horas por usuario
│   ├── HoursByCardTable.tsx              # Tabla horas por tarjeta
│   ├── EmptyState.tsx                    # Estado vacío
│   └── UserDetailModal.tsx               # Modal de detalle
├── services/
│   └── report.service.ts                 # Cliente API
└── types/
    └── report.ts                         # Tipos TypeScript
```

---

## 🔌 Backend - API Endpoints

### 1. GET /report/{board_id}/summary

**Descripción:** Obtiene el resumen semanal de un tablero.

**Parámetros:**
- `board_id` (path): ID del tablero
- `week` (query): Semana en formato ISO `YYYY-WW` (ejemplo: `2026-03`)

**Response:**
```json
{
  "week": "2026-01",
  "completed": {
    "count": 5,
    "items": [
      {
        "id": 123,
        "title": "Implementar login",
        "responsible_id": 1
      }
    ]
  },
  "new": {
    "count": 3,
    "items": [...]
  },
  "overdue": {
    "count": 2,
    "items": [...]
  }
}
```

**Definiciones:**
- **Completadas:** Tarjetas con `completed_at` dentro de la semana O en lista "Hecho" con `updated_at` en la semana
- **Nuevas:** Tarjetas con `created_at` dentro de la semana
- **Vencidas:** Tarjetas con `due_date` en la semana Y NO completadas

**Seguridad:**
- ✅ JWT requerido
- ✅ Usuario debe ser owner o miembro del tablero

---

### 2. GET /report/{board_id}/hours-by-user

**Descripción:** Obtiene horas trabajadas agregadas por usuario.

**Parámetros:**
- `board_id` (path): ID del tablero
- `week` (query): Semana en formato ISO `YYYY-WW`

**Response:**
```json
[
  {
    "user_id": 1,
    "user_name": "Juan Pérez",
    "total_hours": 32.5,
    "tasks_count": 5
  },
  {
    "user_id": 2,
    "user_name": "María García",
    "total_hours": 28.0,
    "tasks_count": 4
  }
]
```

**Campos:**
- `user_id`: ID del usuario
- `user_name`: Nombre del usuario
- `total_hours`: Suma de horas trabajadas en la semana (SUM de `worklogs.hours`)
- `tasks_count`: Número de tarjetas distintas en las que trabajó (COUNT DISTINCT)

**Seguridad:**
- ✅ JWT requerido
- ✅ Usuario debe ser owner o miembro del tablero

---

### 3. GET /report/{board_id}/hours-by-card

**Descripción:** Obtiene horas trabajadas agregadas por tarjeta.

**Parámetros:**
- `board_id` (path): ID del tablero
- `week` (query): Semana en formato ISO `YYYY-WW`

**Response:**
```json
[
  {
    "card_id": 123,
    "title": "Implementar dashboard",
    "responsible": "Juan Pérez",
    "status": "En progreso",
    "total_hours": 12.5
  },
  {
    "card_id": 124,
    "title": "Diseñar mockups",
    "responsible": "María García",
    "status": "Hecho",
    "total_hours": 8.0
  }
]
```

**Ordenamiento:** Por `total_hours` descendente (mayor a menor).

**Campos:**
- `card_id`: ID de la tarjeta
- `title`: Título de la tarjeta
- `responsible`: Nombre del responsable (puede ser null)
- `status`: Nombre de la lista actual de la tarjeta
- `total_hours`: Suma de horas trabajadas en la tarjeta durante la semana

**Seguridad:**
- ✅ JWT requerido
- ✅ Usuario debe ser owner o miembro del tablero

---

## 📅 Cálculo de Semana ISO

### Función: `get_week_date_range(week: str)`

**Ubicación:** `backend/app/report/services.py:22-84`

**Entrada:** Semana en formato `YYYY-WW` (ejemplo: `2026-03`)

**Salida:** Tupla `(start_date: date, end_date: date)`

**Lógica:**

```python
from datetime import date
import re

def get_week_date_range(week: str) -> tuple[date, date]:
    # Validar formato: YYYY-WW
    if not re.match(r"^\d{4}-\d{2}$", week):
        raise HTTPException(400, "Formato inválido. Use 'YYYY-WW'")
    
    year_str, week_str = week.split("-")
    year = int(year_str)
    week_number = int(week_str)
    
    # ISO calendar: lunes = día 1, domingo = día 7
    start_date = date.fromisocalendar(year, week_number, 1)
    end_date = date.fromisocalendar(year, week_number, 7)
    
    return start_date, end_date
```

**Ejemplos:**
- `2026-01` → `(2025-12-29, 2026-01-04)` (Semana 1 de 2026)
- `2026-03` → `(2026-01-12, 2026-01-18)` (Semana 3 de 2026)

**Nota importante:** El formato usado es `YYYY-WW` **sin la letra "W" intermedia**. Esto difiere de algunos estándares que usan `YYYY-W##`, pero es más simple para parsing.

---

## 🗄️ Consultas SQL Utilizadas

### Summary - Tareas Completadas

```sql
SELECT * FROM cards
WHERE board_id = ?
  AND (
    (completed_at IS NOT NULL 
     AND completed_at >= ? 
     AND completed_at <= ?)
    OR
    (list_id = ? -- ID de lista "Hecho"
     AND completed_at IS NULL
     AND updated_at >= ?
     AND updated_at <= ?)
  )
LIMIT 10;
```

### Summary - Tareas Nuevas

```sql
SELECT * FROM cards
WHERE board_id = ?
  AND created_at >= ?
  AND created_at <= ?
LIMIT 10;
```

### Summary - Tareas Vencidas

```sql
SELECT * FROM cards
WHERE board_id = ?
  AND due_date IS NOT NULL
  AND due_date >= ?
  AND due_date <= ?
  AND completed_at IS NULL
  AND list_id != ? -- NO en lista "Hecho"
LIMIT 10;
```

### Hours by User

```sql
SELECT 
  u.id AS user_id,
  u.name AS user_name,
  COALESCE(SUM(te.hours), 0) AS total_hours,
  COUNT(DISTINCT te.card_id) AS tasks_count
FROM users u
  INNER JOIN time_entries te ON te.user_id = u.id
  INNER JOIN cards c ON c.id = te.card_id
WHERE c.board_id = ?
  AND te.date >= ?
  AND te.date <= ?
GROUP BY u.id, u.name;
```

### Hours by Card

```sql
SELECT 
  c.id AS card_id,
  c.title AS title,
  u.name AS responsible,
  l.name AS status,
  COALESCE(SUM(te.hours), 0) AS total_hours
FROM cards c
  INNER JOIN time_entries te ON te.card_id = c.id
  INNER JOIN lists l ON l.id = c.list_id
  LEFT OUTER JOIN users u ON u.id = c.responsible_id
WHERE c.board_id = ?
  AND te.date >= ?
  AND te.date <= ?
GROUP BY c.id, c.title, u.name, l.name
ORDER BY SUM(te.hours) DESC;
```

---

## 🎨 Frontend - Componentes

### ReportPage

**Ubicación:** `frontend_t/src/pages/ReportPage.tsx`

**Responsabilidades:**
- Orquestar carga de datos de 3 endpoints
- Gestionar estado de loading/error
- Renderizar componentes hijos
- Manejar selector de semana
- Exportar CSV

**Estado:**
```typescript
const [week, setWeek] = useState<string>(getCurrentWeek());
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [summary, setSummary] = useState<WeeklySummaryResponse | null>(null);
const [hoursByCard, setHoursByCard] = useState<HoursByCardItem[]>([]);
const [hoursByUser, setHoursByUser] = useState<HoursByUserItem[]>([]);
const [selectedUser, setSelectedUser] = useState<{ id: number; name: string } | null>(null);
```

**Cálculo de Semana Actual:**
```typescript
function getCurrentWeek(): string {
  const now = new Date();
  const target = new Date(now.valueOf());
  
  // Ajustar al jueves de la semana ISO
  const dayNum = (target.getDay() + 6) % 7;
  target.setDate(target.getDate() - dayNum + 3);
  
  // Primer jueves del año
  const firstThursday = new Date(target.getFullYear(), 0, 4);
  const dayOffset = (firstThursday.getDay() + 6) % 7;
  firstThursday.setDate(firstThursday.getDate() - dayOffset + 3);
  
  // Calcular diferencia en semanas
  const weekNumber = Math.ceil(
    (target.getTime() - firstThursday.getTime()) / (7 * 24 * 60 * 60 * 1000)
  ) + 1;
  
  const isoYear = target.getFullYear();
  return `${isoYear}-${String(weekNumber).padStart(2, "0")}`;
}
```

---

### EmptyState

**Ubicación:** `frontend_t/src/components/report/EmptyState.tsx`

**Props:**
```typescript
interface EmptyStateProps {
  message: string;
  icon?: string;
}
```

**Uso:**
```typescript
<EmptyState message="No hubo actividad registrada en esta semana" />
```

Se muestra cuando:
- `summary.completed.count === 0`
- `summary.new.count === 0`
- `summary.overdue.count === 0`
- `hoursByUser.length === 0`
- `hoursByCard.length === 0`

---

### UserDetailModal

**Ubicación:** `frontend_t/src/components/report/UserDetailModal.tsx`

**Props:**
```typescript
interface UserDetailModalProps {
  userId: number;
  userName: string;
  week: string;
  boardId: number;
  onClose: () => void;
}
```

**Funcionalidad:**
- Modal overlay con fondo oscuro
- Cierra al hacer clic fuera o en botón "X"
- Muestra worklogs del usuario en la semana
- **Nota:** Implementación actual usa datos de `hours-by-card` como workaround. Para detalle completo con fecha/nota de cada registro, se recomienda crear endpoint específico `/report/{board_id}/user/{user_id}/worklogs?week=`

---

## 🔐 Seguridad y Permisos

### Matriz de Permisos

| Acción | Owner del Tablero | Miembro del Tablero | Usuario Ajeno |
|--------|-------------------|---------------------|---------------|
| Ver summary | ✅ | ✅ | ❌ (403) |
| Ver hours-by-user | ✅ | ✅ | ❌ (403) |
| Ver hours-by-card | ✅ | ✅ | ❌ (403) |
| Sin JWT | ❌ (401) | ❌ (401) | ❌ (401) |

### Implementación en Backend

**Función:** `verify_board_access(db, board_id, user_id)`  
**Ubicación:** `backend/app/report/services.py:87-142`

```python
def verify_board_access(db: Session, board_id: int, user_id: int) -> None:
    board = db.query(Board).filter(Board.id == board_id).first()
    
    if not board:
        raise HTTPException(404, "Tablero no encontrado.")
    
    # Caso 1: Owner
    if board.user_id == user_id:
        return
    
    # Caso 2: Miembro
    membership = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()
    
    if not membership:
        raise HTTPException(403, "No tienes acceso a este tablero.")
    
    return
```

**Llamada en cada endpoint:**
```python
@router.get("/{board_id}/summary")
def get_weekly_summary(..., current_user=Depends(get_current_user)):
    verify_board_access(db, board_id, current_user.id)  # ← Validación
    # ... resto del código
```

---

## ⚠️ Casos Límite

### 1. Semana sin Datos

**Escenario:** Semana seleccionada no tiene actividad.

**Comportamiento Backend:**
```json
{
  "week": "2026-10",
  "completed": { "count": 0, "items": [] },
  "new": { "count": 0, "items": [] },
  "overdue": { "count": 0, "items": [] }
}
```

**Comportamiento Frontend:**
- Muestra componente `EmptyState`
- Mensaje: "No hubo actividad registrada en esta semana"

---

### 2. Tarjetas sin Responsable

**Escenario:** Tarjeta no tiene `responsible_id` asignado.

**Comportamiento:**
- En `hours-by-card`, el campo `responsible` será `null`
- Frontend debe manejar con fallback: `"Sin asignar"`

---

### 3. Tarjetas sin Horas

**Escenario:** Tarjeta existe pero no tiene worklogs en la semana.

**Comportamiento:**
- NO aparece en `hours-by-card` (solo se incluyen tarjetas CON worklogs)
- Puede aparecer en `summary` si fue completada/creada/vencida

---

### 4. Formato de Semana Inválido

**Input:** `2026-W03` (con "W" intermedia) o `2026/03` (barra)

**Response:**
```json
{
  "detail": "Formato de semana inválido. Use 'YYYY-WW' (ejemplo: 2026-03)."
}
```

**Status:** 400 Bad Request

---

### 5. Semana Inexistente

**Input:** `2026-54` (semana 54 no existe en el año)

**Response:**
```json
{
  "detail": "Semana ISO inválida."
}
```

**Status:** 400 Bad Request

---

### 6. Usuario Removido del Tablero

**Escenario:** Usuario era miembro pero fue removido.

**Comportamiento:**
- Al intentar acceder al informe, recibe 403
- No puede ver datos históricos del tablero

---

### 7. Cambio de Lista "Hecho"

**Escenario:** Tablero no tiene lista llamada exactamente "Hecho".

**Comportamiento:**
- Backend busca lista con `name == "Hecho"`
- Si no existe, solo usa `completed_at` para determinar completadas
- **Recomendación:** Asegurar que cada tablero tenga lista "Hecho" al crearse

---

## ⚡ Optimización y Performance

### Índices Recomendados

```sql
-- Worklogs por tarjeta (acelera JOIN)
CREATE INDEX idx_time_entries_card_id ON time_entries(card_id);

-- Worklogs por usuario (acelera JOIN)
CREATE INDEX idx_time_entries_user_id ON time_entries(user_id);

-- Worklogs por fecha (acelera filtrado semanal)
CREATE INDEX idx_time_entries_date ON time_entries(date);

-- Tarjetas por tablero (ya existe generalmente)
CREATE INDEX idx_cards_board_id ON cards(board_id);

-- Tarjetas por lista (útil para "Hecho")
CREATE INDEX idx_cards_list_id ON cards(list_id);

-- Tarjetas por fecha de creación
CREATE INDEX idx_cards_created_at ON cards(created_at);

-- Tarjetas por fecha de vencimiento
CREATE INDEX idx_cards_due_date ON cards(due_date);
```

### Estrategias de Optimización

1. **Filtrar por board_id primero:** Reduce dataset inicial
2. **Usar agregaciones SQL:** Evitar procesar en Python
3. **LIMIT en items de summary:** Solo top 10 tarjetas por bloque
4. **Lazy loading en frontend:** Cargar tabs bajo demanda (si se implementan)
5. **Caching de semana actual:** Posible cache de 5-15 minutos en backend (opcional)

---

## 🧪 Testing

### Tests de Seguridad

**Archivo:** `backend/tests/test_report_security.py`

**Casos cubiertos:**
- ✅ Endpoints sin token (401)
- ✅ Acceso a tablero ajeno (403)
- ✅ Miembro puede acceder (200)
- ✅ Owner puede acceder (200)
- ✅ Tablero inexistente (404)

**Ejecutar:**
```bash
pytest backend/tests/test_report_security.py -v
```

---

### Tests de Integración

**Archivo:** `backend/tests/test_report_integration.py`

**Casos cubiertos:**
- ✅ Flujo completo con BD real
- ✅ Crear worklog refleja en informe
- ✅ Cambiar semana filtra correctamente
- ✅ Editar tarjeta refleja en summary
- ✅ Semana sin datos retorna vacío

**Ejecutar:**
```bash
pytest backend/tests/test_report_integration.py -v
```

---

### Tests de Servicios

**Archivo:** `backend/tests/test_report_services.py`

**Casos cubiertos:**
- ✅ Cálculo de rango de semana ISO válido
- ✅ Formato inválido rechazado
- ✅ Semana inexistente rechazada

**Ejecutar:**
```bash
pytest backend/tests/test_report_services.py -v
```

---

## 🎬 Guía de Prueba Manual

### Preparación

1. **Asegurar backend corriendo:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Asegurar frontend corriendo:**
   ```bash
   cd frontend_t
   npm run dev
   ```

3. **Tener datos de prueba:**
   - Usuario con login
   - Tablero con listas ("Por hacer", "En progreso", "Hecho")
   - Tarjetas en diferentes listas
   - Worklogs registrados en la semana actual

---

### Flujo de Prueba Completa

#### Paso 1: Login

1. Ir a `http://localhost:5173/login`
2. Ingresar credenciales
3. Verificar redirección a `/boards`

---

#### Paso 2: Navegar a Informe

1. Seleccionar un tablero
2. Buscar enlace/botón "Ver Informe" o ir a `/report/:boardId`
3. Verificar que carga la página

---

#### Paso 3: Verificar Resumen Semanal

**Validar:**
- ✅ Semana actual se muestra por defecto
- ✅ Tarjetas completadas muestran count correcto
- ✅ Tarjetas nuevas muestran count correcto
- ✅ Tarjetas vencidas muestran count correcto
- ✅ Badges de color (verde, azul, rojo) son visibles

---

#### Paso 4: Verificar Horas por Usuario

**Validar:**
- ✅ Tabla muestra usuarios con horas
- ✅ Total de horas es correcto (comparar con DB si es necesario)
- ✅ Número de tareas es correcto
- ✅ Botón "Ver detalle" existe
- ✅ Al hacer clic, se abre modal con información del usuario

---

#### Paso 5: Verificar Horas por Tarjeta

**Validar:**
- ✅ Tabla muestra tarjetas con horas
- ✅ Tarjetas ordenadas de mayor a menor horas
- ✅ Responsable se muestra (o "Sin asignar")
- ✅ Estado/lista actual es correcto

---

#### Paso 6: Exportar CSV

**Validar:**
- ✅ Botón "Exportar CSV" existe para ambas tablas
- ✅ Al hacer clic, descarga archivo CSV
- ✅ Archivo se llama `horas-por-usuario-YYYY-WW.csv` o `horas-por-tarjeta-YYYY-WW.csv`
- ✅ Abrir en Excel: datos se ven correctamente (UTF-8 BOM funciona)
- ✅ Columnas tienen headers correctos

---

#### Paso 7: Cambiar Semana

**Validar:**
- ✅ Input de semana permite edición
- ✅ Cambiar a semana pasada (ej: `2025-52`)
- ✅ Datos se actualizan automáticamente
- ✅ Si semana sin datos, muestra EmptyState

---

#### Paso 8: Semana Inválida

**Validar:**
- ✅ Ingresar formato inválido: `2026-W03` (con W)
- ✅ Muestra mensaje de error claro
- ✅ Ingresar semana inexistente: `2026-54`
- ✅ Muestra mensaje de error claro

---

#### Paso 9: Acceso No Autorizado (Opcional)

**Validar:**
- ✅ Cambiar `boardId` en URL a un tablero que no pertenezca al usuario
- ✅ Debe mostrar error 403 o mensaje "No tienes acceso"

---

### Checklist de QA

- [ ] Resumen semanal carga correctamente
- [ ] Horas por usuario muestra datos correctos
- [ ] Horas por tarjeta muestra datos correctos
- [ ] Exportar CSV funciona para ambas tablas
- [ ] Cambiar semana actualiza datos
- [ ] EmptyState se muestra cuando no hay datos
- [ ] Modal de detalle de usuario funciona
- [ ] Loading state se muestra durante carga
- [ ] Mensajes de error son claros
- [ ] Seguridad: no se puede acceder a tableros ajenos
- [ ] Formato de semana se valida correctamente

---

## 📝 Notas Finales

### Mejoras Futuras Recomendadas

1. **Endpoint dedicado para detalle de usuario:**
   ```
   GET /report/{board_id}/user/{user_id}/worklogs?week=YYYY-WW
   ```
   Retornaría worklogs individuales con fecha, nota, tarjeta.

2. **Filtros adicionales:**
   - Por usuario específico
   - Por rango de fechas custom
   - Por lista/estado

3. **Gráficos visuales:**
   - Gráfico de barras: horas por usuario
   - Gráfico de líneas: evolución semanal
   - Pie chart: distribución de tareas por estado

4. **Comparativa de semanas:**
   - Comparar semana actual vs anterior
   - Mostrar tendencias (↑ ↓)

5. **Exportar PDF:**
   - Informe completo en PDF para impresión

---

**Versión del Documento:** 1.0  
**Autor:** Equipo NeoCare  
**Última Revisión:** 13 de Enero 2026

