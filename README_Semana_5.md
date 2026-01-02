# 📊 Semana 5 — Informe Semanal & Extras
## NeoCare Health — Kanban + Timesheets Lite · FastAPI + React

**Duración:** lunes–viernes  
**Objetivo general:** Construir la vista **Informe Semanal**, que permite al departamento de Innovación de NeoCare visualizar en un solo panel el progreso del equipo, y añadir funcionalidades extra (**Etiquetas, Subtareas y Búsqueda**) para mejorar la gestión de tarjetas.

---

## 1. Introducción
Después de implementar tarjetas, drag & drop y registro de horas, el objetivo de esta semana es convertir esos datos en información útil. El informe semanal permite monitorizar el avance, detectar bloqueos y analizar la distribución del esfuerzo. Además, se han incorporado "Extras" para enriquecer la experiencia de usuario y la organización del trabajo.

---

## 2. Roles y responsabilidades de la semana

### 👑 Coordinador/a
- ✓ Definir las métricas finales del informe.
- ✓ Asegurar la coherencia entre frontend ↔ backend ↔ SQL.
- ✓ Supervisar la implementación de los **Extras** (Labels, Subtasks).
- ✓ Validar que las consultas SQL de agregación son eficientes.
- ✓ Preparar la demo final del producto.

### 💻 Frontend
Implementar la página de Informe Semanal y las mejoras en las tarjetas:
- **Informe Semanal (/report):**
    - ✓ Selector de semana (YYYY-WW).
    - ✓ Bloque **Resumen**: Tareas completadas, vencidas y nuevas.
    - ✓ Bloque **Horas por Persona**: Tabla con totales de horas y conteo de tareas.
    - ✓ Bloque **Horas por Tarjeta**: Tabla ordenada por esfuerzo (horas desc).
    - ✓ Exportación a **CSV**.
- **Extras:**
    - ✓ Gestión de **Etiquetas** (colores y nombres) en el detalle de la tarjeta.
    - ✓ Checklist de **Subtareas** con estado de completado.
    - ✓ Barra de **Búsqueda** y filtro por **Responsable** en el tablero.

### ⚙️ Backend (FastAPI)
Construir consultas SQL optimizadas y nuevos endpoints para extras:
- **Módulo de Informes (`/reports`):**
    - `GET /reports/summary?week=...` → Estadísticas de tarjetas (Completadas, Vencidas, Nuevas).
    - `GET /reports/hours-by-user?board_id=...` → Agregación de horas por usuario.
    - `GET /reports/hours-by-card?board_id=...` → Agregación de horas por tarjeta.
- **Módulo de Extras (Labels & Subtasks):**
    - `POST /cards/{id}/labels` y `DELETE /labels/{id}`.
    - `POST /cards/{id}/subtasks`, `PATCH /subtasks/{id}` y `DELETE /subtasks/{id}`.
- **Búsqueda y Filtros:**
    - Mejora de `GET /cards/` para soportar parámetros `search` (ilike) y `responsible_id`.

### 🧪 Testing
- ✓ Pruebas de agregación SQL: Verificar que los totales de horas coinciden con los registros individuales.
- ✓ Pruebas de seguridad: Validar que un usuario no puede ver informes de tableros ajenos.
- ✓ Pruebas de integración: Crear horas y verificar su reflejo inmediato en el informe.
- ✓ Validación de los Extras: Crear etiquetas y subtareas asociadas correctamente a la tarjeta.

---

## 3. Modelo de Datos (Ampliación)
### Tabla `labels`
- `id` SERIAL PRIMARY KEY
- `card_id` INTEGER REFERENCES cards(id)
- `name` VARCHAR(50)
- `color` VARCHAR(20)

### Tabla `subtasks`
- `id` SERIAL PRIMARY KEY
- `card_id` INTEGER REFERENCES cards(id)
- `title` VARCHAR(200)
- `completed` BOOLEAN DEFAULT FALSE
- `position` INTEGER DEFAULT 0

---

## 4. Definition of Done (Checklist)
- [x] **Backend:** Endpoints de informes con lógica de semanas ISO, CRUD de etiquetas y subtareas, filtros de búsqueda.
- [x] **Frontend:** Vista `/report` completa, exportación CSV funcional, UI para etiquetas y subtareas.
- [x] **Testing:** 100% de éxito en pruebas de totales y seguridad.
- [x] **Documentación:** README de Semana 5, Postman actualizado con la nueva colección "Semana 5 + Extras".

---

## 5. Criterios de Aceptación (QA)
1. Puedo seleccionar una semana y ver el resumen de tarjetas (Nuevas/Vencidas/Hechas).
2. Los totales de horas por usuario y tarjeta son exactos.
3. Puedo exportar los datos a un archivo CSV.
4. Puedo añadir múltiples etiquetas de colores a una tarjeta.
5. Puedo crear una lista de subtareas y marcarlas como completadas.
6. La búsqueda por título filtra las tarjetas del tablero en tiempo real.
7. El sistema impide el acceso a informes de tableros donde el usuario no es miembro.
