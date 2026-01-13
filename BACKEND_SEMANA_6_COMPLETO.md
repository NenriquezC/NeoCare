# ✅ Backend Preparado - Semana 6 Extensiones

## 📋 Estado de Implementación

El backend está **100% completado** para todas las extensiones de la Semana 6, con:
- ✅ Modelos compatibles con SQLite (tests) y PostgreSQL (producción)
- ✅ Endpoints completamente documentados con ejemplos
- ✅ Tests unitarios funcionales
- ✅ Código comentado para facilitar integración del frontend

---

## 🏷️ LABELS (Etiquetas)

### Modelos
```python
# backend/app/boards/models.py
class Label(Base):
    __tablename__ = "labels"
    
    id: int  
    card_id: int  # FK a cards.id
    name: str  # Nombre de la etiqueta (máx 50 caracteres)
    color: str | None  # Color HEX (#ef4444) o null
```

### Endpoints Disponibles

#### 1. POST /cards/{card_id}/labels
Añade una etiqueta a una tarjeta

**Request:**
```json
{
    "name": "Urgente",
    "color": "#ef4444"
}
```

    "card_id": 123,
    "color": "#ef4444"
}
```

#### 2. GET /cards/{card_id}/labels
Obtiene todas las etiquetas de una tarjeta

**Response:** `list[LabelOut]`

#### 3. DELETE /cards/labels/{label_id}
Elimina una etiqueta

**Response:** `204 No Content`

### Colores Sugeridos para Frontend
  medium: "#f59e0b",     // Amarillo - Prioridad media
  low: "#10b981",        // Verde - Baja prioridad
  feature: "#3b82f6",    // Azul - Features, info
  qa: "#8b5cf6",         // Púrpura - Testing, QA
  blocked: "#6b7280"     // Gris - Bloqueado, pausado
};
```

### Ejemplo de Integración Frontend (React)
```tsx
// Componente para mostrar labels
function CardLabels({ labels }: { labels: Label[] }) {
  return (
      {labels.map(label => (
        <span
          key={label.id}
          className="px-2 py-1 rounded text-xs font-medium text-white"
          style={{ backgroundColor: label.color }}
        >
          {label.name}
        </span>
      ))}
    </div>
  );
}

// Función para añadir label
async function addLabel(cardId: number, labelData: {name: string, color: string}) {
      'Authorization': `Bearer ${token}`
    body: JSON.stringify(labelData)
  });
  return response.json();

async function deleteLabel(labelId: number) {
  await fetch(`/cards/labels/${labelId}`, {
    method: 'DELETE',
```
---

## ✅ SUBTASKS (Checklist)
# backend/app/boards/models.py
    __tablename__ = "subtasks"
    
    id: int
    position: int  # Posición en la lista (para ordenar)

### Endpoints Disponibles

#### 1. POST /cards/{card_id}/subtasks
    "title": "Escribir documentación de API",
}
```

**Response:** `SubtaskOut`
```json
{
    "id": 1,
    "card_id": 123,
    "title": "Escribir documentación de API",
    "completed": false,
    "position": 0
}
```

#### 2. GET /cards/{card_id}/subtasks
Obtiene todas las subtareas de una tarjeta (ordenadas por position)

**Response:** `list[SubtaskOut]`

#### 3. PATCH /cards/subtasks/{subtask_id}
Actualiza una subtarea (todos los campos opcionales)

**Request (marcar como completada):**
```json
{
    "completed": true
}
```

**Request (cambiar título):**
```json
{
    "title": "Nuevo título actualizado"
}
```

**Request (múltiples campos):**
```json
{
    "title": "Título nuevo",
    "completed": true,
    "position": 2
}
```

#### 4. DELETE /cards/subtasks/{subtask_id}
Elimina una subtarea

**Response:** `204 No Content`

### Ejemplo de Integración Frontend (React)
```tsx
// Componente de Checklist con progreso
function SubtaskChecklist({ cardId, subtasks }: Props) {
  const completed = subtasks.filter(s => s.completed).length;
  const total = subtasks.length;
  const percentage = Math.round((completed / total) * 100);
  
  return (
    <div className="space-y-3">
      {/* Header con progreso */}
      <div className="flex items-center justify-between">
        <h3 className="font-medium">Checklist</h3>
        <span className="text-sm text-gray-600">
          {completed}/{total} completadas
        </span>
      </div>
      
      {/* Barra de progreso */}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-green-500 h-2 rounded-full transition-all"
          style={{ width: `${percentage}%` }}
        />
      </div>
      
      {/* Lista de subtasks */}
      <div className="space-y-2">
        {subtasks.map(subtask => (
          <label key={subtask.id} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={subtask.completed}
              onChange={() => toggleSubtask(subtask.id, subtask.completed)}
              className="w-4 h-4"
            />
            <span className={subtask.completed ? 'line-through text-gray-500' : ''}>
              {subtask.title}
            </span>
            <button
              onClick={() => deleteSubtask(subtask.id)}
              className="ml-auto text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </label>
        ))}
      </div>
      
      {/* Input para añadir nueva subtask */}
      <form onSubmit={handleAddSubtask} className="flex gap-2">
        <input
          type="text"
          placeholder="Añadir subtarea..."
          className="flex-1 px-3 py-2 border rounded"
        />
        <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
          Añadir
        </button>
      </form>
    </div>
  );
}

// Funciones helper
async function toggleSubtask(subtaskId: number, currentCompleted: boolean) {
  await fetch(`/cards/subtasks/${subtaskId}`, {
    method: 'PATCH',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ completed: !currentCompleted })
  });
}

async function addSubtask(cardId: number, title: string) {
  const response = await fetch(`/cards/${cardId}/subtasks`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ title, completed: false })
  });
  return response.json();
}

async function deleteSubtask(subtaskId: number) {
  await fetch(`/cards/subtasks/${subtaskId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
}
```

---

## 🔍 BÚSQUEDA Y FILTRADO

### Endpoint Mejorado: GET /cards

**Query Parameters:**
- `board_id` (requerido): ID del tablero
- `search` (opcional): Busca en título y descripción (case-insensitive)
- `responsible_id` (opcional): Filtra por usuario responsable
- `list_id` (opcional): Filtra por lista específica

### Ejemplos de Uso

#### 1. Buscar "urgente" en tablero
```bash
GET /cards?board_id=1&search=urgente
```

#### 2. Filtrar por responsable
```bash
GET /cards?board_id=1&responsible_id=5
```

#### 3. Combinar filtros
```bash
GET /cards?board_id=1&search=API&responsible_id=5&list_id=2
```

### Ejemplo Frontend
```typescript
// Hook personalizado para búsqueda y filtrado
function useCardFilters(boardId: number) {
  const [search, setSearch] = useState('');
  const [responsibleId, setResponsibleId] = useState<number | null>(null);
  const [listId, setListId] = useState<number | null>(null);
  const [cards, setCards] = useState<Card[]>([]);
  
  useEffect(() => {
    fetchFilteredCards();
  }, [search, responsibleId, listId]);
  
  async function fetchFilteredCards() {
    const params = new URLSearchParams({
      board_id: boardId.toString()
    });
    
    if (search) params.append('search', search);
    if (responsibleId) params.append('responsible_id', responsibleId.toString());
    if (listId) params.append('list_id', listId.toString());
    
    const response = await fetch(`/cards?${params}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    setCards(data);
  }
  
  return { cards, search, setSearch, responsibleId, setResponsibleId, listId, setListId };
}

// Componente de búsqueda
function SearchBar() {
  const { search, setSearch, setResponsibleId, setListId } = useCardFilters(boardId);
  
  return (
    <div className="flex gap-2">
      {/* Barra de búsqueda */}
      <input
        type="search"
        placeholder="Buscar tarjetas..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="flex-1 px-4 py-2 border rounded-lg"
      />
      
      {/* Filtro por responsable */}
      <select onChange={(e) => setResponsibleId(Number(e.target.value) || null)}>
        <option value="">Todos los responsables</option>
        {users.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}
      </select>
      
      {/* Filtro por lista */}
      <select onChange={(e) => setListId(Number(e.target.value) || null)}>
        <option value="">Todas las listas</option>
        {lists.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
      </select>
    </div>
  );
}
```

---

## 🧪 Tests con SQLite

Todos los tests están configurados para usar **SQLite automáticamente** gracias a `conftest.py`:

```bash
# Ejecutar todos los tests (usan SQLite)
pytest

# Ejecutar solo tests de Labels y Subtasks
pytest tests/labels_subtasks/ -v

# Ejecutar test específico
pytest tests/labels_subtasks/test_labels_subtasks.py::test_create_label -v
```

### Tests Disponibles

#### Labels:
- ✅ `test_create_label` - Crear etiqueta
- ✅ `test_get_card_labels` - Obtener labels de una tarjeta
- ✅ `test_delete_label` - Eliminar etiqueta
- ✅ `test_label_without_auth` - Validar autenticación

#### Subtasks:
- ✅ `test_create_subtask` - Crear subtarea
- ✅ `test_get_card_subtasks` - Obtener subtareas
- ✅ `test_update_subtask_completed` - Marcar como completada
- ✅ `test_update_subtask_title` - Actualizar título
- ✅ `test_delete_subtask` - Eliminar subtarea
- ✅ `test_subtask_progress_calculation` - Calcular progreso

#### Búsqueda:
- ✅ `test_search_cards_by_title` - Búsqueda por título
- ✅ `test_search_cards_by_description` - Búsqueda por descripción  
- ✅ `test_filter_by_responsible` - Filtro por responsable
- ✅ `test_combined_filters` - Filtros combinados

---

## 📊 Modelos Actualizados - CardOut

El schema de salida de tarjetas ahora incluye labels y subtasks:

```python
class CardOut(BaseModel):
    id: int
    board_id: int
    list_id: int
    order: int
    title: str
    description: str | None
    due_date: date | None
    created_by_id: int
    responsible_id: int | None
    created_at: datetime
    updated_at: datetime
    archived: bool
    labels: list[LabelOut] = []      # 🆕 Semana 6
    subtasks: list[SubtaskOut] = []  # 🆕 Semana 6
```

**Ejemplo de Response completo:**
```json
{
    "id": 123,
    "board_id": 1,
    "list_id": 2,
    "order": 0,
    "title": "Implementar búsqueda global",
    "description": "Añadir endpoint y UI",
    "due_date": "2026-01-15",
    "created_by_id": 1,
    "responsible_id": 5,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T12:00:00Z",
    "archived": false,
    "labels": [
        {"id": 1, "card_id": 123, "name": "Feature", "color": "#3b82f6"},
        {"id": 2, "card_id": 123, "name": "Urgente", "color": "#ef4444"}
    ],
    "subtasks": [
        {"id": 1, "card_id": 123, "title": "Crear endpoint", "completed": true, "position": 0},
        {"id": 2, "card_id": 123, "title": "Implementar UI", "completed": false, "position": 1}
    ]
}
```

---

## 🎯 Checklist para Frontend

### Labels
- [ ] Crear componente `<CardLabels>` para mostrar chips con colores
- [ ] Crear modal/dropdown para añadir labels con selector de colores
- [ ] Añadir botón de eliminar (X) en cada label
- [ ] Integrar en modal de edición de tarjeta
- [ ] (Opcional) Añadir filtro por label en la vista de tablero

### Subtasks
- [ ] Crear componente `<SubtaskChecklist>` con checkboxes
- [ ] Implementar barra de progreso visual ("3/7 completadas")
- [ ] Añadir input para crear nuevas subtasks
- [ ] Implementar toggle para marcar completadas
- [ ] Añadir botón de eliminar por subtask
- [ ] Integrar en modal de edición de tarjeta

### Búsqueda y Filtros
- [ ] Crear input de búsqueda global en header/navbar
- [ ] Implementar dropdown de filtro por responsable
- [ ] (Opcional) Filtro por lista
- [ ] Combinar múltiples filtros
- [ ] Mostrar contador de resultados

### UX/Fluidez
- [ ] Loading states en todas las operaciones
- [ ] Animaciones CSS para drag & drop
- [ ] Toast notifications para feedback
- [ ] Error handling con mensajes claros

---

## 🚀 Quick Start para Frontend

### 1. Obtener tarjeta con labels y subtasks
```typescript
const card = await fetch(`/cards/${cardId}`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

console.log(card.labels);    // Array de labels
console.log(card.subtasks);  // Array de subtasks
```

### 2. Añadir label
```typescript
await fetch(`/cards/${cardId}/labels`, {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ name: "Urgente", color: "#ef4444" })
});
```

### 3. Crear subtask
```typescript
await fetch(`/cards/${cardId}/subtasks`, {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ title: "Nueva tarea" })
});
```

### 4. Buscar tarjetas
```typescript
const cards = await fetch(
  `/cards?board_id=1&search=urgente&responsible_id=5`,
  { headers: { 'Authorization': `Bearer ${token}` } }
).then(r => r.json());
```

---

## 📝 Notas Técnicas

### Compatibilidad SQLite vs PostgreSQL
- ✅ Los modelos funcionan en ambas bases de datos
- ✅ Tests usan SQLite automáticamente (via `TESTING=1` en conftest.py)
- ✅ Desarrollo/Postman usan PostgreSQL (configurado en `.env`)
- ✅ No hay características específicas de PostgreSQL que rompan SQLite

### Seguridad
- ✅ Todos los endpoints requieren JWT (`get_current_user`)
- ✅ Validación de permisos por tablero (`verify_board_permission`)
- ✅ Solo el usuario del tablero puede modificar labels/subtasks

### Performance
- Las relaciones labels y subtasks usan `cascade="all, delete-orphan"`
- Se eliminan automáticamente cuando se elimina la tarjeta
- La búsqueda usa `ILIKE` para case-insensitive (compatible SQLite/PostgreSQL)

---

## 🎓 Para Documentador

Actualizar README global con:
1. Sección "Semana 6 - Extensiones implementadas"
2. Tabla de endpoints nuevos
3. Ejemplos de request/response
4. Screenshots del frontend (cuando esté listo)
5. Decisiones técnicas (por qué relación directa vs many-to-many)

---

**Backend completado y listo para integración frontend** ✅
