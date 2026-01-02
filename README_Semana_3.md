# 📋 Semana 3 — Drag & Drop y Sincronización de Estado
## NeoCare Health — Kanban + Timesheets Lite · FastAPI + React

**Duración:** lunes–viernes  
**Objetivo general:** Implementar el movimiento de tarjetas entre columnas mediante Drag & Drop, actualizar la base de datos en tiempo real y reforzar la usabilidad del tablero. Al finalizar esta semana, los usuarios de NeoCare podrán arrastrar una tarjeta y moverla a otra columna con fluidez.

---

## 1. Introducción
Tras completar la creación y edición de tarjetas, esta semana el reto es convertir el tablero en una herramienta dinámica y visualmente atractiva. NeoCare necesita que los equipos de Innovación puedan reorganizar fácilmente sus tareas según prioridad y estado.

**En Semana 3 haremos:**
- ✓ Activar el arrastre de tarjetas.
- ✓ Permitir soltarlas en otras columnas.
- ✓ Actualizar `list_id` y `order` en la base de datos.
- ✓ Mantener el orden dentro de cada columna.
- ✓ Mejorar la claridad visual del tablero.

---

## 2. Roles y responsabilidades de la semana

### 👑 Coordinador/a
- ✓ Asegurar que frontend y backend definen la misma estructura para ordenamiento.
- ✓ Coordinar pruebas cruzadas.
- ✓ Verificar que las decisiones de ordenamiento se documentan.
- ✓ Supervisar backlog y riesgos.
- ✓ Dar el OK final a la demo del viernes.

### 💻 Frontend
Responsable principal del Drag & Drop:
- **Tareas principales:**
    - ✓ Instalar y configurar `dnd-kit`.
    - ✓ Hacer que `CardItem` sea draggable.
    - ✓ Habilitar `ListColumn` como zona “droppable”.
    - ✓ Detectar eventos: Inicio, movimiento y soltado.
    - ✓ Actualizar la UI localmente (Optimistic UI).
    - ✓ Enviar al backend: `list_id` (destino) y `order` (posición).
- **UX/UI:**
    - ✓ Evitar saltos visuales e indicar placeholders.
    - ✓ Estilos para tarjeta en movimiento (opacidad, sombra, escala).
- **Integración:**
    - ✓ Llamar al endpoint `/cards/{id}/move`.
    - ✓ Manejar errores (revertir estado si falla la API).

### ⚙️ Backend (FastAPI)
Implementar la lógica sólida del movimiento de tarjetas:
- **Extensión del modelo:** Añadir campo `order` (INTEGER) a la tabla `cards`.
- **Endpoint de movimiento:** `PATCH /cards/{id}/move`.
- **Lógica interna:**
    - ✓ Validar propiedad y acceso al tablero destino.
    - ✓ Actualizar `list_id` y `order`.
    - ✓ Reordenar las demás tarjetas afectadas (estrategia de shift).
    - ✓ Mantener integridad de orden.
- **Seguridad:** Token JWT obligatorio.

### 🧪 Testing
- ✓ Verificar actualización de `list_id` al arrastrar.
- ✓ Confirmar persistencia del orden tras recargar.
- ✓ Probar soltar en distintos puntos (inicio, mitad, final).
- ✓ Simular errores: Sin token, card no encontrada, tablero ajeno.
- ✓ Revisión de fluidez visual y ausencia de duplicados.

### 📝 Documentador
- ✓ Documentar funcionamiento del Drag & Drop y estrategia de ordenamiento.
- ✓ Añadir ejemplos de payload para el nuevo endpoint `/move`.
- ✓ Escribir acta semanal completa.
- ✓ Preparar guion de mini-demo (mostrar arrastre real).

---

## 3. Arquitectura Técnica

### Frontend (React + dnd-kit)
- **Componentes clave:** `BoardView.tsx`, `ListColumn.tsx`, `CardItem.tsx`.
- **Flujo:** Arrastre -> Cálculo local -> Actualización UI -> Petición API -> Confirmación/Reversión.

### Backend (FastAPI)
- **Endpoint:** `PATCH /cards/{id}/move`.
- **Estrategia de orden:** El equipo debe elegir y documentar si usará orden incremental (0,1,2...) o saltos (10,20,30...).

---

## 4. Definition of Done (Checklist)
- [ ] **Backend:** Campo `order` añadido, endpoint `/move` operativo, lógica de reordenamiento validada.
- [ ] **Frontend:** Drag & Drop funcional y suave, persistencia tras recarga, manejo de errores.
- [ ] **Testing:** Movimiento validado en todas las columnas, sin tarjetas perdidas.
- [ ] **Documentación:** README actualizado, acta semanal y mini-demo lista.

---

## 5. Criterios de Aceptación (QA)
1. Puedo arrastrar una tarjeta y soltarla en otra columna.
2. El cambio se refleja visualmente de inmediato.
3. El backend actualiza `list_id` y `order` sin inconsistencias.
4. Tras recargar, el orden se mantiene.
5. No se crean duplicados de tarjetas.
6. Error visual claro si la API falla.
