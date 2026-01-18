# Semana 5 — Informe Semanal

**NeoCare Health — Kanban + Timesheets Lite · FastAPI + React**

**Duración:** lunes–viernes

## Objetivo general

Construir la vista **Informe Semanal**, que permitirá al departamento de Innovación de NeoCare visualizar en un solo panel:

✓ Tareas completadas durante la semana  
✓ Tareas vencidas  
✓ Nuevas tareas creadas  
✓ Horas trabajadas por persona  
✓ Horas trabajadas por tarjeta  
✓ Totales agregados  
✓ Exportación a CSV  

Este módulo es clave porque proporciona la visibilidad real que NeoCare necesita para evaluar el progreso, detectar bloqueos y planificar recursos.

---

## Introducción

Después de implementar tarjetas, drag & drop y registro de horas, esta semana el objetivo es dar sentido a todos esos datos: **convertirlos en insight**.

El informe semanal permitirá a NeoCare:

✓ Monitorizar el avance de cada proyecto  
✓ Detectar tareas atrasadas  
✓ Calcular la carga de trabajo real  
✓ Analizar distribución del esfuerzo por persona y tarea  
✓ Presentar métricas claras en las reuniones de seguimiento  

Este módulo es la base de la demo final y de la utilidad práctica del producto.

---

## Roles y responsabilidades de la semana

### Coordinador/a

✓ Definir junto al equipo las métricas finales del informe  
✓ Asegurar la coherencia entre frontend ↔ backend ↔ SQL  
✓ Coordinar pruebas y tiempos  
✓ Supervisar que las consultas SQL funcionan correctamente  
✓ Aprobar la estructura final de la vista del informe  
✓ Preparar y revisar la mini-demo del viernes  

### Frontend

Implementa toda la página **Informe semanal**.

#### Tareas principales

✓ Crear la ruta `/report`  
✓ Crear selector de semana (por defecto semana actual)  
✓ Mostrar los siguientes bloques:

**1. Resumen de la semana**
- ✔ Número de tareas completadas
- ✔ Número de tareas vencidas
- ✔ Nuevas tareas creadas
- ✔ Listas cortas de cada grupo con:
  - Título
  - Responsable
  - Estado

**Badges de colores:**
- ✓ Verde → completadas
- ✓ Rojo → vencidas
- ✓ Azul → nuevas

**2. Horas por persona**

Tabla con:
- ✓ Usuario
- ✓ Total de horas (semana actual)
- ✓ Nº total de tareas en las que trabajó
- ✓ Acción para ver detalle

**3. Horas por tarjeta**

Tabla con:
- ✓ Título de tarjeta
- ✓ Responsable
- ✓ Estado actual
- ✓ Total de horas
- ✓ Ordenar por horas (desc)

**4. Exportación CSV**
- ✓ Exportar tabla de horas por persona
- ✓ Exportar horas por tarjeta (opcional)

#### Interacciones necesarias

✓ Peticiones a múltiples endpoints  
✓ Mostrar estados vacíos ("No hubo tareas completadas esta semana")  
✓ Manejo de errores  
✓ Indicadores de carga mientras se generan resultados  

### Backend (FastAPI)

El backend deberá construir consultas SQL optimizadas para rango semanal.

#### Cálculo del rango semanal

Desde frontend se enviará:
```
week=YYYY-WW
```

Backend debe calcular:
- ✓ Inicio de la semana (lunes)
- ✓ Fin de la semana (domingo)

#### Endpoints requeridos

**✔ GET /report/{board_id}/summary?week=**

Devuelve:
- ✓ Completadas
- ✓ Vencidas
- ✓ Nuevas

Basado en:

**Completadas**
- ✓ cards.list_id = 'Hecho'
- ✓ cards.updated_at ∈ semana seleccionada

**Vencidas**
- ✓ due_date ∈ semana
- ✓ list_id != 'Hecho'

**Nuevas**
- ✓ created_at ∈ semana

**✔ GET /report/{board_id}/hours-by-user?week=**

Devuelve:
- ✓ user_id
- ✓ total_hours
- ✓ tasks_count

Agrupación:
```sql
SUM(worklogs.hours)
COUNT(DISTINCT card_id)
```

**✔ GET /report/{board_id}/hours-by-card?week=**

Devuelve:
- ✓ card_id
- ✓ total_hours
- ✓ responsible
- ✓ estado
- ✓ título

Agrupación:
```sql
SUM(worklogs.hours)
```

#### Validaciones

✓ El usuario solo puede ver informes de sus tableros  
✓ Semana válida  
✓ Manejo de rangos sin datos  

### Testing

#### Pruebas del panel Resumen

✓ Tareas completadas se calculan correctamente  
✓ Nuevas tareas se identifican bien  
✓ Vencidas son correctas  

#### Pruebas de horas

✓ Totales por persona correctos  
✓ Totales por tarjeta correctos  
✓ Filtrado por semana funciona  
✓ Exportación CSV contiene los datos correctos  

#### Pruebas de seguridad

✓ No se puede consultar informes de otro usuario  
✓ JWT obligatorio  

#### Pruebas de integración

✓ Crear horas → ver reflejo en informe  
✓ Editar tarjeta → ver cambios en estado en informe  
✓ Cambiar semana → actualizar resultados  

### Documentador

✓ Actualizar README con:
  - Consultas SQL utilizadas
  - Endpoints /report
  - Ejemplos de respuesta
  - Cómo calcular la semana en el frontend

✓ Documentar casos límite:
  - Semana sin datos
  - Tareas sin responsable
  - Tarjetas sin horas

✓ Redactar acta semanal  
✓ Preparar guion de demo  

---

## Lógica y estructura del Informe Semanal

### 1. Cálculo del rango semanal

El sistema debe convertir "YYYY-WW" en:
- ✓ Fecha lunes
- ✓ Fecha domingo

### 2. Agrupaciones clave

✓ Por estado  
✓ Por responsable  
✓ Por tarjeta  
✓ Por fecha  

### 3. Optimización

✓ Uso de índices en worklogs.card_id, worklogs.user_id  
✓ Minimizar joins innecesarios  
✓ Uso de agregaciones SQL  

### 4. Estructura recomendada del frontend

```
/report
  ├── SummarySection
  ├── HoursByUserTable
  ├── HoursByCardTable
  ├── WeekSelector
  └── ExportButtons
```

---

## Definition of Done (Checklist)

### ✔ Backend
- ➢ Endpoints summary / hours-by-user / hours-by-card
- ➢ Cálculo correcto de la semana
- ➢ Consultas SQL optimizadas
- ➢ Seguridad correcta

### ✔ Frontend
- ➢ Vista completa del informe
- ➢ Selector de semana
- ➢ Resumen visual claro
- ➢ Tablas de datos ordenables
- ➢ Exportación CSV
- ➢ Mensajes de estado vacío
- ➢ Manejo de errores

### ✔ Testing
- ➢ Totales correctos
- ➢ Seguridad validada
- ➢ Semanas sin datos correctamente manejadas

### ✔ Documentación
- ➢ README actualizado
- ➢ Acta semanal
- ➢ Mini-demo lista

---

## Criterios de aceptación (QA)

NeoCare considerará la semana completada cuando:

1. Puedo seleccionar una semana y ver:
   - Completadas
   - Vencidas
   - Nuevas

2. Los totales de horas por usuario son correctos.

3. Los totales de horas por tarjeta son correctos.

4. Puedo exportar la tabla a CSV.

5. Los estados vacíos muestran mensajes claros.

6. El informe responde en menos de 2 segundos con 100+ registros.

7. No permite accesos no autorizados.

---

## Plan de trabajo sugerido (lunes–viernes)

### Día 1 — Diseño del informe + cálculo de semana
✓ Backend: lógica de fechas  
✓ Frontend: maqueta de /report  

### Día 2 — Bloque Resumen
✓ Cálculo completadas / nuevas / vencidas  
✓ Frontend render inicial  

### Día 3 — Horas por persona
✓ Endpoint y tabla  
✓ Totales correctos  

### Día 4 — Horas por tarjeta + CSV
✓ Tabla avanzada  
✓ Exportación CSV  
✓ Estados vacíos  

### Día 5 — QA + demo
✓ Pruebas completas  
✓ README actualizado  
✓ Acta semanal  
✓ Presentación interna  

---

## Revisión del lunes siguiente

Cada equipo debe mostrar:

✓ El informe semanal con datos reales  
✓ Totales correctos  
✓ Exportación funcional  
✓ Explicación técnica:
  - Consultas SQL
  - Endpoints
  - Cálculo de semana
✓ README y documentación actualizada  

El coordinador presentará el acta y el plan de la **Semana 6 — Extras útiles**.
