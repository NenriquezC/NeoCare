# 📋 Semana 4 — Registro de horas (Timesheets)
## NeoCare Health — Kanban + Timesheets Lite · FastAPI + React

**Duración:** lunes–viernes  
**Objetivo general:** Incorporar el sistema de registro de horas trabajadas por cada miembro del equipo en las tarjetas del tablero. Cada usuario de NeoCare podrá registrar cuántas horas ha dedicado a una tarea, en qué fecha y con qué detalles.

---

## 1. Introducción
La productividad y el seguimiento de esfuerzo son elementos clave en el departamento de Innovación de NeoCare. Los responsables necesitan saber qué tareas tienen mayor carga, quién está dedicando más horas y qué parte del trabajo se realiza semana a semana.

**Al finalizar esta semana, debe existir una funcionalidad completa para:**
- ✓ Añadir horas.
- ✓ Ver horas por tarjeta.
- ✓ Editar horas propias.
- ✓ Eliminar horas propias.
- ✓ Consultar horas totales en una vista personal.

---

## 2. Roles y responsabilidades de la semana

### 👑 Coordinador/a
- ✓ Coordinar el diseño del modelo `worklogs`.
- ✓ Asegurar que backend y frontend usan los mismos campos.
- ✓ Supervisar que las validaciones (horas > 0, fecha válida) se cumplan.
- ✓ Validar que los permisos están correctamente configurados.
- ✓ Asegurar que la demo del viernes muestra el flujo completo.

### 💻 Frontend
Implementar la UI de Timesheets:
- **Tareas principales:**
    - ✓ Añadir sección “Horas trabajadas” dentro de la vista de tarjeta.
    - ✓ Crear formulario para registrar una hora (Fecha, Horas mín 0.25h, Nota).
    - ✓ Mostrar listado de worklogs de la tarjeta.
    - ✓ Permitir editar y eliminar un worklog propio.
    - ✓ Crear nueva vista “Mis horas” en el menú principal (Listado semanal, totales por día y total semanal).
- **Integraciones:**
    - ✓ Consumir endpoints del backend.
    - ✓ Validar: Horas > 0, Fecha válida, Nota ≤ 200 chars.
    - ✓ Refrescar la tarjeta tras cambios.

### ⚙️ Backend (FastAPI)
Crear toda la infraestructura del sistema de worklogs:
- **Modelo SQLAlchemy (Tabla `worklogs` / `time_entries`):**
    - `id`, `card_id`, `user_id`, `date`, `hours`, `note`, `created_at`, `updated_at`.
- **Endpoints implementados:**
    - `POST /worklogs/` → Crear registro (con `card_id` en body).
    - `GET /worklogs/card/{card_id}` → Listar por tarjeta.
    - `PATCH /worklogs/{id}` → Editar horas (actualización parcial).
    - `DELETE /worklogs/{id}` → Eliminar horas.
    - `GET /worklogs/me/week?week=YYYY-WW` → Horas por semana del usuario actual.
- **Validaciones obligatorias:**
    - Horas > 0 (mínimo recomendado 0.25).
    - Fecha válida y no futura.
    - Nota ≤ 200 chars.
    - Solo el autor puede editar/borrar su registro.

**📚 Documentación Completa:** Ver `WORKLOGS_API_GUIDE.md` para guía exhaustiva con ejemplos de cURL, Postman, validaciones, permisos y casos límite.

### 🧪 Testing
- ✓ Validar creación de worklogs válidos e inválidos.
- ✓ Pruebas de seguridad: No permitir editar/eliminar registros ajenos.
- ✓ Pruebas de integración: Flujo completo desde creación de tarjeta hasta totales semanales.

### 📝 Documentador
- ✓ Actualizar README con la nueva tabla y endpoints.
- ✓ Documentar permisos y casos límite.
- ✓ Redactar acta semanal y preparar guion para mini-demo.

---

## 3. Modelo de Datos (PostgreSQL)
### Tabla `worklogs` (implementada como `time_entries`)
- `id` SERIAL PRIMARY KEY
- `card_id` INTEGER REFERENCES cards(id)
- `user_id` INTEGER REFERENCES users(id)
- `date` DATE NOT NULL
- `hours` FLOAT NOT NULL
- `note` VARCHAR(200)
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()

---

## 4. Definition of Done (Checklist)
- [x] **Backend:** Tabla creada, endpoints CRUD funcionando, seguridad por usuario aplicada.
- [x] **Frontend:** Formulario de horas, listado por tarjeta, vista "Mis horas" con totales.
- [x] **Testing:** Casos límite probados, seguridad validada, tests E2E implementados.
- [x] **Documentación:** README completo, `WORKLOGS_API_GUIDE.md` exhaustiva con ejemplos Postman/cURL.

**Estado:** ✅ **COMPLETADO** (13 Enero 2026)  
**Tests Adicionales:** 6 tests de seguridad agregados  
**Mejoras:** Cambio de PUT a PATCH según estándar REST

---

## 5. Criterios de Aceptación (QA)
1. Puedo añadir horas a una tarjeta desde su detalle.
2. Puedo ver un listado cronológico de horas por tarjeta.
3. Puedo editar o eliminar solo mis horas.
4. Las validaciones funcionan (horas > 0, nota <= 200 chars).
5. En “Mis horas” veo mis horas filtradas por semana con totales correctos.
