# 🎯 Componentes Frontend - Tablero Kanban Mejorado

## 📋 Descripción General

Este documento describe los componentes visuales implementados para mejorar el tablero Kanban con funcionalidades avanzadas de gestión de tareas.

---

## 🎨 Componentes Principales

### 1. **CardsBoard.tsx** ⭐ Componente Maestro
- **Ubicación:** `frontend_t/src/components/cards/CardsBoard.tsx`
- **Función:** Componente principal que orquesta todo el tablero Kanban
- **Características:**
  - Gestión completa de tarjetas (CRUD)
  - Integración de todos los filtros y búsqueda
  - Estado compartido entre componentes
  - Modal avanzado para crear/editar tarjetas
  - Columnas Kanban mejoradas con animaciones

#### Estados Principales:
```typescript
- cards[]              // Lista de tarjetas del tablero
- searchText          // Búsqueda global
- selectedLabels[]    // Filtros por etiquetas
- selectedAssignee    // Filtro por responsable
- form                // Datos del formulario (con labels y checklist)
```

---

### 2. **SearchBar.tsx** 🔍 Búsqueda Global
- **Props:**
  - `value: string` - Texto de búsqueda actual
  - `onChange: (value: string) => void` - Callback de cambio
  - `placeholder?: string` - Placeholder personalizado
  - `resultsCount?: number` - Cantidad de resultados
  - `totalCount?: number` - Total de tarjetas

- **Características:**
  - Búsqueda en tiempo real (título + descripción)
  - Interfaz limpia con iconos
  - Indicador de resultados
  - Botón para limpiar búsqueda

---

### 3. **LabelManager.tsx** 🏷️ Gestor de Etiquetas
- **Props:**
  - `labels: Label[]` - Etiquetas asignadas a la tarjeta
  - `onAddLabel: (label) => void` - Agregar etiqueta
  - `onRemoveLabel: (labelId) => void` - Eliminar etiqueta
  - `presetLabels: Label[]` - Etiquetas disponibles

- **Colores disponibles:**
  - 🔵 Blue (Mejora)
  - 🔴 Red (Urgente)
  - 🟢 Green (Listo)
  - 🟡 Yellow (Bloqueado)
  - 🟣 Purple (Feature)
  - 🩷 Pink (Bug)
  - 🟦 Indigo (Documentación)
  - 🟠 Orange (Review)

- **Características:**
  - Selector visual de etiquetas
  - Chips interactivos
  - Eliminación de etiquetas

---

### 4. **LabelFilter.tsx** 🎯 Filtro por Etiquetas
- **Props:**
  - `selectedLabels: string[]` - IDs de etiquetas seleccionadas
  - `onLabelToggle: (labelId) => void` - Toggle de etiqueta
  - `availableLabels: Label[]` - Etiquetas para filtrar

- **Características:**
  - Dropdown con checkboxes
  - Contador de filtros activos
  - Visualización de colores en filtro
  - Opción para limpiar todos los filtros

---

### 5. **ChecklistManager.tsx** ✅ Gestor de Checklists
- **Props:**
  - `items: ChecklistItem[]` - Items del checklist
  - `onAddItem: (item) => void` - Agregar item
  - `onToggleItem: (itemId) => void` - Marcar/desmarcar
  - `onRemoveItem: (itemId) => void` - Eliminar item

- **Características:**
  - Agregar items con Enter
  - Marcar como completado
  - Eliminar items
  - Barra de progreso visual
  - Porcentaje de completitud

---

### 6. **ChecklistProgress.tsx** 📊 Barra de Progreso
- **Props:**
  - `items: ChecklistItem[]` - Items del checklist

- **Características:**
  - Barra visual de progreso
  - Porcentaje completado
  - Contador visual (3/5)

---

### 7. **AssigneeFilter.tsx** 👤 Filtro por Responsable
- **Props:**
  - `selectedAssignee: string | null` - ID del responsable
  - `onAssigneeChange: (assigneeId) => void` - Cambiar responsable
  - `teamMembers: TeamMember[]` - Lista de miembros

- **Características:**
  - Dropdown con miembros del equipo
  - Avatares visuales
  - Mostrar/ocultar todas las tarjetas
  - Selección con estado visual

---

### 8. **CardItem.tsx** 📇 Item de Tarjeta Mejorado
- **Props:**
  - `card: Card` - Datos de la tarjeta
  - `onEdit: (card) => void` - Callback de edición
  - `isSelected?: boolean` - Estado de selección

- **Características:**
  - Muestra etiquetas con colores
  - Barra de progreso del checklist
  - Información de fecha límite con emoji
  - Efecto hover mejorado
  - Botón editar con transición suave

---

### 9. **LabelChip.tsx** 💅 Componente de Etiqueta Visual
- **Props:**
  - `label: Label` - Etiqueta a mostrar
  - `onRemove?: () => void` - Callback de eliminación
  - `interactive?: boolean` - Modo interactivo

- **Características:**
  - Colores predefinidos según tipo
  - Botón X para eliminar (en modo interactivo)
  - Bordes y estilos visuales

---

## 🔄 Flujo de Datos

```
CardsBoard
  ├── SearchBar → setSearchText
  ├── LabelFilter → setSelectedLabels[]
  ├── AssigneeFilter → setSelectedAssignee
  ├── Filtered Cards (useMemo) ← Aplica todos los filtros
  └── Columnast
      └── CardItem[]
          ├── onEdit → openEdit
          └── Modal con:
              ├── LabelManager
              ├── ChecklistManager
              └── AssigneeSelect
```

---

## 🎯 Funcionalidades Implementadas

### ✅ Búsqueda Global
- Busca en título y descripción
- Resultados en tiempo real
- Indicador de cantidad

### ✅ Filtro por Etiquetas
- Selector visual
- Múltiples etiquetas simultáneamente
- Colores predefinidos
- Lógica OR (muestra si tiene CUALQUIER etiqueta seleccionada)

### ✅ Filtro por Responsable
- Dropdown con miembros del equipo
- Avatares
- Opción "Mostrar todas"

### ✅ Checklists
- Agregar/editar/eliminar items
- Marcar como completado
- Barra de progreso visual
- Porcentaje de avance

### ✅ Etiquetas Visuales
- 8 colores predefinidos
- Chips interactivos
- Gestión en modal

### ✅ Mejoras Visuales
- Animaciones suaves
- Transiciones en hover
- Gradientes en headers
- Iconos descriptivos
- Responsive design
- ScrollBar personalizado

---

## 🎨 Estilos y Animaciones

### Animaciones CSS
```css
- fadeIn: Entrada suave
- slideUp: Deslizamiento hacia arriba
- scaleIn: Escalado desde centro
- pulse: Parpadeo suave
- card-hover: Elevación al pasar mouse
```

### Colores Principales
- **Blue**: `#3b82f6` (primario)
- **Green**: `#16a34a` (éxito)
- **Red**: `#dc2626` (peligro)
- **Yellow**: `#eab308` (advertencia)

---

## 📱 Responsive Design

- ✅ Mobile: 1 columna
- ✅ Tablet: 2-3 columnas
- ✅ Desktop: 3 columnas
- ✅ Scrollbar personalizado en todas las plataformas

---

## 🔧 Constantes Globales

### Etiquetas Predefinidas
```typescript
const PRESET_LABELS = [
  { id: "urgent", name: "Urgente", color: "red" },
  { id: "blocked", name: "Bloqueado", color: "yellow" },
  { id: "improve", name: "Mejora", color: "blue" },
  { id: "ready", name: "Listo", color: "green" },
  // ... 4 más
]
```

### Miembros del Equipo
```typescript
const TEAM_MEMBERS = [
  { id: "user1", name: "Juan Pérez", avatar: "..." },
  { id: "user2", name: "María García", avatar: "..." },
  // ... más miembros
]
```

---

## 📌 Notas Importantes

1. **Backend Integration**: Los componentes están listos para integrarse con el backend. Actualmente, las etiquetas y checklists se envían junto con la tarjeta.

2. **Estados Locales**: Los filtros son locales (no persistentes). Para persistencia, enviar al backend.

3. **Avatares**: Usan Dicebear API para generar avatares automáticamente.

4. **Performance**: Uso de `useMemo` para optimizar filtrado.

---

## 🚀 Próximas Mejoras (Opcional)

- [ ] Drag & drop entre columnas
- [ ] Filtro por múltiples responsables
- [ ] Guardar filtros en localStorage
- [ ] Historial de cambios
- [ ] Comentarios en tarjetas
- [ ] Notificaciones en tiempo real
- [ ] Exportar tablero a PDF

---

## 📝 Licencia

Todos los componentes están listos para uso en producción.
