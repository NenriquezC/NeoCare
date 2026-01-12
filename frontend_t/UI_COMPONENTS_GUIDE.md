# 🎨 Guía de Componentes UI - NeoCare

Esta guía muestra cómo usar los componentes de pulido visual implementados.

---

## 1. 🔄 Loading (Spinners y Estados de Carga)

### Spinner Simple
```tsx
import { Spinner } from '@/components/ui/Loading';

// Diferentes tamaños
<Spinner size="sm" />  // Pequeño
<Spinner size="md" />  // Mediano (default)
<Spinner size="lg" />  // Grande
```

### Page Loader (Pantalla completa)
```tsx
import { PageLoader } from '@/components/ui/Loading';

function MiComponente() {
  const [loading, setLoading] = useState(true);
  
  if (loading) return <PageLoader />;
  
  return <div>Contenido...</div>;
}
```

### Loading Overlay
```tsx
import { LoadingOverlay } from '@/components/ui/Loading';

{isProcessing && <LoadingOverlay message="Guardando cambios..." />}
```

### Loading Button
```tsx
import { LoadingButton } from '@/components/ui/Loading';

<LoadingButton
  loading={isSubmitting}
  onClick={handleSubmit}
  className="px-4 py-2 bg-blue-600 text-white rounded"
>
  Guardar
</LoadingButton>
```

---

## 2. 📭 Empty States (Estados Vacíos)

### Empty State Genérico
```tsx
import { EmptyState } from '@/components/ui/EmptyState';

<EmptyState
  title="No hay resultados"
  description="Intenta con otros filtros"
  action={{
    label: "Limpiar filtros",
    onClick: () => resetFilters()
  }}
/>
```

### Empty States Específicos

#### Sin Tarjetas
```tsx
import { NoCardsEmpty } from '@/components/ui/EmptyState';

{cards.length === 0 && (
  <NoCardsEmpty onCreateCard={() => setShowCreateModal(true)} />
)}
```

#### Sin Horas Registradas
```tsx
import { NoWorklogsEmpty } from '@/components/ui/EmptyState';

{worklogs.length === 0 && <NoWorklogsEmpty />}
```

#### Sin Tableros
```tsx
import { NoBoardsEmpty } from '@/components/ui/EmptyState';

{boards.length === 0 && <NoBoardsEmpty />}
```

#### Sin Datos Genérico
```tsx
import { NoDataEmpty } from '@/components/ui/EmptyState';

<NoDataEmpty message="No hay informes disponibles" />
```

---

## 3. 🔔 Toast (Notificaciones)

### Uso Básico
```tsx
import { toast } from '@/components/ui/Toast';

// Success
toast.success('Tarjeta creada correctamente');

// Error
toast.error('No se pudo guardar los cambios');

// Info
toast.info('Se actualizó la información');

// Warning
toast.warning('Esta acción es irreversible');
```

### En Funciones Async
```tsx
async function handleSave() {
  try {
    await api.save(data);
    toast.success('✅ Guardado correctamente');
  } catch (error) {
    toast.error('❌ Error al guardar');
  }
}
```

### Container (ya integrado en App.tsx)
El `<ToastContainer />` ya está añadido en App.tsx, no necesitas importarlo en cada página.

---

## 📝 Ejemplos de Uso Completo

### Login con Loading y Toast
```tsx
import { useState } from 'react';
import { LoadingButton } from '@/components/ui/Loading';
import { toast } from '@/components/ui/Toast';

export function Login() {
  const [loading, setLoading] = useState(false);
  
  async function handleLogin(e) {
    e.preventDefault();
    setLoading(true);
    
    try {
      await api.login(email, password);
      toast.success('Bienvenido a NeoCare! 👋');
      navigate('/board');
    } catch (error) {
      toast.error('Credenciales incorrectas');
    } finally {
      setLoading(false);
    }
  }
  
  return (
    <form onSubmit={handleLogin}>
      {/* ... campos ... */}
      <LoadingButton loading={loading} type="submit">
        Iniciar Sesión
      </LoadingButton>
    </form>
  );
}
```

### Lista con Loading y Empty State
```tsx
import { useState, useEffect } from 'react';
import { PageLoader } from '@/components/ui/Loading';
import { NoCardsEmpty } from '@/components/ui/EmptyState';

export function CardsList() {
  const [loading, setLoading] = useState(true);
  const [cards, setCards] = useState([]);
  
  useEffect(() => {
    loadCards();
  }, []);
  
  async function loadCards() {
    try {
      const data = await api.getCards();
      setCards(data);
    } catch (error) {
      toast.error('Error al cargar tarjetas');
    } finally {
      setLoading(false);
    }
  }
  
  if (loading) return <PageLoader />;
  
  if (cards.length === 0) {
    return <NoCardsEmpty onCreateCard={() => setShowModal(true)} />;
  }
  
  return (
    <div>
      {cards.map(card => (
        <CardItem key={card.id} card={card} />
      ))}
    </div>
  );
}
```

### Operación con Overlay
```tsx
import { useState } from 'react';
import { LoadingOverlay } from '@/components/ui/Loading';
import { toast } from '@/components/ui/Toast';

export function DeleteCard({ cardId }) {
  const [deleting, setDeleting] = useState(false);
  
  async function handleDelete() {
    if (!confirm('¿Eliminar esta tarjeta?')) return;
    
    setDeleting(true);
    
    try {
      await api.deleteCard(cardId);
      toast.success('Tarjeta eliminada');
    } catch (error) {
      toast.error('No se pudo eliminar');
    } finally {
      setDeleting(false);
    }
  }
  
  return (
    <>
      {deleting && <LoadingOverlay message="Eliminando tarjeta..." />}
      <button onClick={handleDelete}>Eliminar</button>
    </>
  );
}
```

---

## 🎨 Personalización

### Spinner Custom
```tsx
<Spinner size="lg" className="border-red-600" />
```

### Toast con Iconos
```tsx
toast.success('✅ Guardado');
toast.error('❌ Error');
toast.info('ℹ️ Información');
toast.warning('⚠️ Advertencia');
```

### Empty State Personalizado
```tsx
<EmptyState
  icon={<MiIconoCustom />}
  title="Título custom"
  description="Descripción"
  action={{
    label: "Acción",
    onClick: handleAction
  }}
/>
```

---

## ✅ Checklist de Integración

Actualizar páginas existentes:

- [ ] **Login.tsx**: Añadir LoadingButton y toast
- [ ] **Board.tsx**: Añadir PageLoader y NoCardsEmpty
- [ ] **Worklogs.tsx**: Añadir NoWorklogsEmpty
- [ ] **Reports.tsx**: Añadir NoDataEmpty
- [ ] **CardsBoard.tsx**: Añadir estados de carga en operaciones

---

## 🚀 Próximos Pasos

1. Reemplazar botones normales por `LoadingButton`
2. Añadir `PageLoader` en carga inicial de datos
3. Reemplazar `alert()` por `toast.success/error()`
4. Añadir empty states donde falten
5. Añadir `LoadingOverlay` en operaciones críticas (delete, move)

---

**Documentación actualizada:** 12 Enero 2026
