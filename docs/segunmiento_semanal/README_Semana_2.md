# 📋 Semana 2 — Tarjetas (Cards): Crear, Editar y Mostrar
## NeoCare Health — Kanban + Timesheets Lite · FastAPI + React

**Duración:** lunes–viernes  
**Objetivo general:** Construir el núcleo principal del flujo de trabajo: crear tarjetas, listarlas por columna, editarlas y validarlas, con persistencia real en PostgreSQL. Al finalizar la semana, el tablero debe tener contenido real, no solo columnas vacías.

---

## 1. Introducción
Después de dejar lista la base del proyecto (autenticación, estructura, tablero inicial), esta semana entramos en la funcionalidad central que NeoCare necesita para coordinar sus iniciativas internas: las tarjetas, que representan tareas reales del departamento de Innovación.

**Una tarjeta es la unidad mínima de trabajo, y debe contener:**
- ✓ Título
- ✓ Descripción
- ✓ Responsable (user_id opcional esta semana)
- ✓ Fecha límite (due_date)
- ✓ Estado (columna)
- ✓ Fechas de creación y actualización

Además, debe poder crearse, editarse y visualizarse en las tres columnas del tablero.

---

## 2. Roles y responsabilidades de la semana

### 👑 Coordinador/a
- ✓ Repartir tareas entre frontend/backend/testing.
- ✓ Decidir naming de tablas, columnas y rutas.
- ✓ Asegurar que los endpoints cumplen los criterios de NeoCare.
- ✓ Coordinar integración y pruebas cruzadas.
- ✓ Mantener comunicación diaria.
- ✓ Supervisar la entrega y la mini-demos del viernes.

### 💻 Frontend
Implementar la interfaz completa para tarjetas:
- **Tareas principales:**
    - ✓ Mostrar tarjetas por columnas (fetch a `/cards?board_id=...`).
    - ✓ Crear formulario “Nueva tarjeta”: Título (obligatorio), Descripción, Fecha límite.
    - ✓ Modal o página para Editar tarjeta.
    - ✓ Validaciones: Título requerido (1–80 chars), Fecha límite válida.
    - ✓ Renderizar tarjetas: Título, Estado, Fecha límite (badge si vence pronto).
- **Integraciones:**
    - ✓ Consumir endpoints del backend.
    - ✓ Actualizar lista tras crear/editar.
    - ✓ Usar token JWT en todas las peticiones.
    - ✓ Manejar errores visuales (mensajes claros).

### ⚙️ Backend (FastAPI)
Crear toda la lógica de tarjetas:
- **Modelos SQLAlchemy (Tabla `cards`):**
    - `id`, `board_id` (FK), `list_id` (FK), `title`, `description`, `due_date`, `user_id` (creador), `created_at`, `updated_at`.
- **Endpoints:**
    - `POST /cards` → Crear tarjeta.
    - `GET /cards?board_id=` → Listar por tablero.
    - `GET /cards/{id}` → Ver detalle.
    - `PATCH /cards/{id}` → Editar campos.
    - `DELETE /cards/{id}` (opcional).
- **Validaciones obligatorias:**
    - Título requerido.
    - Fecha límite válida (si existe).
    - El usuario solo puede ver tarjetas de sus tableros.
    - Timestamps automáticos.
- **Seguridad:**
    - Token JWT obligatorio.
    - Verificar permisos por usuario.

### 🧪 Testing
- ✓ Verificar creación de tarjeta (datos válidos, título vacío, fecha inválida).
- ✓ Probar edición de tarjeta.
- ✓ Validar orden de tarjetas en frontend.
- ✓ Revisar errores devueltos por la API.
- ✓ Crear issues en GitHub por cada bug encontrado.
- ✓ Testar flujos reales: Login -> Crear -> Ver -> Editar -> Reflejar cambios.

### 📝 Documentador
- ✓ Actualizar README con nuevos endpoints, validaciones y estructura del modelo.
- ✓ Redactar el acta semanal (logros, bloqueos, decisiones).
- ✓ Preparar guion para mini-demos y documentar criterios de aceptación.

---

## 3. Modelo de Datos (PostgreSQL)
### Tabla `cards`
- `id` SERIAL PRIMARY KEY
- `board_id` INTEGER REFERENCES boards(id)
- `list_id` INTEGER REFERENCES lists(id)
- `title` VARCHAR(80) NOT NULL
- `description` TEXT
- `due_date` DATE
- `user_id` INTEGER REFERENCES users(id)
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()

---

## 4. Definition of Done (Checklist)
- [ ] **Backend:** Tabla creada, endpoints funcionales, validaciones completas, seguridad JWT.
- [ ] **Frontend:** CRUD de tarjetas, visualización por columnas, badges de fecha, actualización inmediata.
- [ ] **Testing:** Casos límite verificados, flujo completo funcionando.
- [ ] **Documentación:** README actualizado, acta semanal lista, mini-demo preparada.

---

## 5. Criterios de Aceptación (QA)
1. Puedo crear una tarjeta y verla aparecer en la columna correcta.
2. Si el título está vacío, el sistema no deja guardarla.
3. Si la fecha no es válida, aparece un mensaje de error.
4. Puedo editar la tarjeta y los cambios se reflejan inmediatamente.
5. Puedo ver tarjetas ordenadas correctamente.
6. El sistema rechaza peticiones sin autorización (sin JWT).
