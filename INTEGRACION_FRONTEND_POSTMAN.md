# 📚 Guía de Integración Frontend - Cambios Backend y Postman

> **Fecha:** 8 de Enero 2026  
> **Estado:** ✅ Backend y Postman 100% funcionales


## 🎯 Resumen Ejecutivo

Se han realizado modificaciones en el backend y la colección de Postman para:
1. ✅ Crear tablas faltantes de Semana 6 (labels y subtasks)
2. ✅ Agregar validadores flexibles para IDs (aceptan strings o números)
3. ✅ Implementar cleanup automático en Postman
4. ✅ Asegurar compatibilidad frontend-backend


## 📋 Cambios en el Backend

### 1. **Tablas Creadas en PostgreSQL**

#### Tabla `labels`
```sql
CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7)  -- Formato HEX: #ef4444
);
```

#### Tabla `subtasks`
```sql
CREATE TABLE subtasks (
    id SERIAL PRIMARY KEY,
    card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT false,
    position INTEGER NOT NULL DEFAULT 0
);
```

**⚠️ IMPORTANTE para Frontend:**

### 2. **Validadores Pydantic Agregados**

Se agregaron validadores en los schemas para **mayor flexibilidad** en el formato de datos:

#### `backend/app/cards/schemas.py`
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator

class CardCreate(BaseModel):
    title: str
    board_id: int
    list_id: int
    # ... otros campos
    
    @field_validator('board_id', 'list_id', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convierte strings a int para compatibilidad con Postman/Newman"""
        if v is None:
            return v
        if isinstance(v, str):
            return int(v)
        return v
```

**Ventajas para el Frontend:**

#### Schemas modificados:

### 3. **Endpoint DELETE /auth/me**

```python
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina el usuario autenticado y todos sus datos relacionados.
    
    Por CASCADE, también elimina:
    - Todos los boards del usuario
    - Todas las listas de esos boards
    - Todas las cards de esos boards
    - Todos los time_entries del usuario
    - Todos los labels y subtasks de las cards
    - Todas las board_memberships del usuario
    """
    try:
        db.delete(current_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )
    return None
```

**Uso desde Frontend:**
```javascript
// Eliminar usuario actual (útil para tests o GDPR)
async function deleteCurrentUser(token) {
    const response = await fetch('http://localhost:8000/auth/me', {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (response.status === 204) {
        console.log('✅ Usuario eliminado completamente');
        // Limpiar localStorage, redirigir a login, etc.
    }
}
```


## 📮 Colección de Postman Modificada

### Archivo: `NeoCare_Postman_Collection_Updated.json`

#### Cambios Realizados:

1. **Variables de Colección Definidas:**
```json
{
  "variable": [
    {"key": "access_token", "value": ""},
    {"key": "user_email", "value": ""},
    {"key": "user_password", "value": ""},
    {"key": "board_id", "value": ""},
    {"key": "list_id", "value": ""},
    {"key": "card_id", "value": ""},
    {"key": "time_entry_id", "value": ""},
    // ... más variables
  ]
}
```

2. **Scripts de Test Optimizados:**

3. **Nuevo Request de Cleanup:**
```json
{
  "name": "🧹 CLEANUP - Eliminar usuario de test",
  "request": {
    "method": "DELETE",
    "url": "http://localhost:8000/auth/me",
    "header": [
      {"key": "Authorization", "value": "Bearer {{access_token}}"}
    ]
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "// Acepta 204 (eliminado) o 401 (ya limpio)",
        "pm.test('Cleanup ejecutado', function () {",
        "    pm.expect([204, 401]).to.include(pm.response.code);",
        "});",
        "",
        "// Limpiar variables",
        "pm.collectionVariables.unset('access_token');",
        "pm.collectionVariables.unset('user_id');",
        "// ... más unset"
      ]
    }
  }]
}
```

### Cómo Ejecutar la Colección:

#### En Postman UI:
1. Importar `NeoCare_Postman_Collection_Updated.json`
2. Abrir Collection Runner
3. Ejecutar la colección completa
4. ✅ Al final, el cleanup elimina automáticamente todos los datos de test

#### Desde Línea de Comandos (Newman):
```bash
newman run NeoCare_Postman_Collection_Updated.json
```

**Resultado Esperado:**
```
✅ 16 requests ejecutados
✅ 16 tests pasados
✅ 0 fallos
✅ Datos de test eliminados automáticamente
```


## 🛠️ Script Auxiliar: `fix_postman.py`

### Ubicación: `backend/fix_postman.py`

**Propósito:**  
Elimina variables locales duplicadas en los scripts de test de Postman (útil si modificas la colección manualmente).

```python
# Uso:
python backend/fix_postman.py

# Output:
# 🔧 Corrigiendo scripts de test...
#   📝 1️⃣ REGISTRO - Crear usuario: 16 → 13 líneas
#   📝 2️⃣ LOGIN - Obtener token: 14 → 11 líneas
# ...
# ✅ Colección corregida
```

**¿Cuándo usarlo?**


## 🔗 Integración con Frontend

### 1. **Formato de Datos Flexible**

El backend ahora acepta IDs tanto como números o strings:

```javascript
// ✅ Ambos formatos funcionan:

// Opción 1: IDs como números
const cardData = {
    title: "Nueva tarjeta",
    board_id: 123,
    list_id: 456,
    description: "Descripción"
};

// Opción 2: IDs como strings (por si vienen de inputs)
const cardData = {
    title: "Nueva tarjeta",
    board_id: "123",
    list_id: "456",
    description: "Descripción"
};

// El backend convierte automáticamente
```

### 2. **Endpoints de Semana 6 Disponibles**

#### Labels (Etiquetas):
```javascript
// Crear label
POST /cards/{card_id}/labels
Body: { "name": "Urgente", "color": "#ef4444" }

// Obtener labels de una tarjeta
GET /cards/{card_id}/labels

// Eliminar label
DELETE /cards/labels/{label_id}
```

#### Subtasks (Checklist):
```javascript
// Crear subtask
POST /cards/{card_id}/subtasks
Body: { "title": "Tarea 1", "completed": false }

// Obtener subtasks
GET /cards/{card_id}/subtasks

// Actualizar subtask
PATCH /cards/subtasks/{subtask_id}
Body: { "completed": true }

// Eliminar subtask
DELETE /cards/subtasks/{subtask_id}
```

### 3. **Búsqueda y Filtrado Mejorado**

```javascript
// Buscar tarjetas con filtros combinados
GET /cards?board_id=1&search=urgente&responsible_id=5&list_id=2

// Ejemplos para el frontend:
const params = new URLSearchParams({
    board_id: boardId.toString()
});

if (searchText) params.append('search', searchText);
if (responsibleId) params.append('responsible_id', responsibleId.toString());
if (listId) params.append('list_id', listId.toString());

const response = await fetch(`/cards?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

### 4. **Cleanup de Datos (Útil para Tests)**

```javascript
// En tests del frontend, limpiar datos automáticamente:
async function cleanupTestData(token) {
    try {
        await fetch('http://localhost:8000/auth/me', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log('✅ Datos de test eliminados');
    } catch (error) {
        console.error('Error en cleanup:', error);
    }
}

// Usar en afterEach o afterAll de tus tests
afterEach(async () => {
    await cleanupTestData(testToken);
});
```


## ⚠️ Consideraciones Importantes

### 1. **CASCADE Deletes**

### 2. **Validación de IDs**

### 3. **Tokens de Autenticación**

### 4. **CORS**
El backend tiene CORS habilitado para todos los orígenes:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En producción, especificar dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


## 📂 Archivos Modificados/Creados

```
NeoCare/
├── backend/
│   ├── app/
│   │   ├── cards/
│   │   │   └── schemas.py           ✏️ MODIFICADO (validadores)
│   │   ├── worklogs/
│   │   │   └── schemas.py           ✏️ MODIFICADO (validadores)
│   │   ├── auth/
│   │   │   └── routes.py            ✏️ MODIFICADO (DELETE /me)
│   │   └── main.py                   ✏️ MODIFICADO (debug=True)
│   ├── alembic/
│   │   └── versions/
│   │       └── semana_6_add_labels_and_subtasks.py  ➕ NUEVO
│   ├── create_semana6_tables.py      ➕ NUEVO
│   ├── create_semana6_tables.sql     ➕ NUEVO
│   └── fix_postman.py                ➕ NUEVO (corregir colección)
│
├── NeoCare_Postman_Collection_Updated.json  ✏️ MODIFICADO
└── INTEGRACION_FRONTEND_POSTMAN.md          ➕ NUEVO (este archivo)
```


## 🚀 Pasos para el Frontend

### Checklist de Integración:

  ```javascript
  const API_URL = 'http://localhost:8000';
  ```

  ```javascript
  const token = localStorage.getItem('access_token');
  headers: { 'Authorization': `Bearer ${token}` }
  ```

  ```typescript
  interface Card {
      id: number;
      title: string;
      board_id: number;
      list_id: number;
      labels: Label[];
      subtasks: Subtask[];
      // ... más campos
  }
  
  interface Label {
      id: number;
      card_id: number;
      name: string;
      color: string | null;
  }
  
  interface Subtask {
      id: number;
      card_id: number;
      title: string;
      completed: boolean;
      position: number;
  }
  ```

  ```javascript
  // services/cards.js
  export async function createCard(cardData, token) {
      const response = await fetch(`${API_URL}/cards/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(cardData)
      });
      
      if (!response.ok) {
          throw new Error(`Error ${response.status}`);
      }
      
      return response.json();
  }
  ```

  ```javascript
  if (response.status === 401) {
      // Token expirado, redirigir a login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
  }
  ```

  - Componente para mostrar/crear labels con colores
  - Componente de checklist para subtasks
  - Barra de progreso para subtasks completadas


## 🧪 Testing

### Tests del Frontend con Cleanup Automático:

```javascript
// tests/integration/cards.test.js
import { describe, it, afterEach, expect } from 'vitest';
import { register, login, deleteUser } from '../services/auth';
import { createCard } from '../services/cards';

describe('Cards API', () => {
    let testToken;
    
    afterEach(async () => {
        // Cleanup automático después de cada test
        if (testToken) {
            await deleteUser(testToken);
            testToken = null;
        }
    });
    
    it('should create a card', async () => {
        // Register y login
        const email = `test${Date.now()}@test.com`;
        await register(email, 'Test123!', 'Test User');
        const { access_token } = await login(email, 'Test123!');
        testToken = access_token;
        
        // Crear tarjeta
        const card = await createCard({
            title: 'Test Card',
            board_id: 1,
            list_id: 1
        }, testToken);
        
        expect(card).toHaveProperty('id');
        expect(card.title).toBe('Test Card');
    });
});
```


## 📞 Soporte

Si encuentras problemas durante la integración:

1. **Verificar que el backend esté corriendo:**
   ```bash
   curl http://localhost:8000/
   # Debe retornar: {"status":"NeoCare Backend Running"}
   ```

2. **Verificar tablas en PostgreSQL:**
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public' 
   AND table_name IN ('labels', 'subtasks');
   ```

3. **Ejecutar colección de Postman:**
   ```bash
   newman run NeoCare_Postman_Collection_Updated.json
   ```

4. **Revisar logs del backend:**
   - El backend ahora tiene `debug=True` activado
   - Los errores 500 mostrarán el traceback completo


## ✅ Conclusión

**Todo está listo para la integración del frontend:**


**No hay problemas para integrar el frontend ahora.**


*Última actualización: 8 de Enero 2026*  
*Estado: ✅ Completado y Probado*
