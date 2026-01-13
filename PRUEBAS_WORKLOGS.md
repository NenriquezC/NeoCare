# 🧪 Guía de Pruebas Rápidas - Módulo Worklogs

## ⚡ Prueba Rápida (5 minutos)

### Pre-requisitos
- ✅ Backend corriendo en `http://127.0.0.1:8000`
- ✅ Frontend corriendo en `http://localhost:5173`
- ✅ Usuario logueado con token válido

---

## 🎯 Prueba 1: Crear Worklog desde Tarjeta

**Pasos:**
1. Ir a `/boards`
2. Click en el tablero
3. Click en cualquier tarjeta **existente** (no nueva)
4. Scroll hasta "⏱️ Horas Trabajadas"
5. Click "+ Registrar horas"
6. **Ingresar:**
   - Fecha: Hoy
   - Horas: `2.5`
   - Nota: "Implementación de worklogs"
7. Click "Guardar"

**Resultado esperado:**
- ✅ Mensaje verde: "✅ Registro guardado"
- ✅ Aparece en la lista con badge azul "2.50h"
- ✅ Muestra fecha formateada
- ✅ Muestra nota
- ✅ Muestra "ID: X · (tú)"
- ✅ Tiene botones de editar y eliminar

---

## 🎯 Prueba 2: Editar Worklog

**Pasos:**
1. En el worklog recién creado, click en icono de lápiz (editar)
2. Cambiar horas a `3.0`
3. Cambiar nota a "Implementación y pruebas"
4. Click "Guardar"

**Resultado esperado:**
- ✅ Mensaje verde: "✅ Registro actualizado"
- ✅ Badge cambia a "3.00h"
- ✅ Nota actualizada visible
- ✅ Vuelve al modo lectura

---

## 🎯 Prueba 3: Validaciones

**Pasos:**
1. Click "+ Registrar horas" otra vez
2. Intentar horas = `0.1` (menor a 0.25)
3. Intentar guardar

**Resultado esperado:**
- ❌ Error: "Las horas deben ser al menos 0.25"

**Pasos continuación:**
4. Cambiar horas a `1.0`
5. Cambiar fecha a mañana (fecha futura)
6. Intentar guardar

**Resultado esperado:**
- ❌ Error: "No se pueden registrar horas en fechas futuras"

---

## 🎯 Prueba 4: Eliminar Worklog

**Pasos:**
1. En un worklog propio, click en icono de basura (eliminar)
2. Confirmar en el diálogo

**Resultado esperado:**
- ✅ Mensaje verde: "✅ Registro eliminado"
- ✅ Worklog desaparece de la lista
- ✅ Total de horas se actualiza

---

## 🎯 Prueba 5: Página "Mis Horas"

**Pasos:**
1. Navegar a `/my-hours` (desde el menú o directamente)
2. Observar la vista

**Resultado esperado:**
- ✅ Muestra semana actual en formato YYYY-WW
- ✅ Muestra total semanal de horas
- ✅ Lista "Totales por día" con fechas
- ✅ Tabla con todos los worklogs del usuario
- ✅ Selector de semana funcional
- ✅ Formulario para crear nuevo worklog

**Pasos continuación:**
3. Cambiar a semana anterior con el selector
4. Verificar que datos se recargan

**Resultado esperado:**
- ✅ Loading indicator
- ✅ Datos actualizados para la nueva semana
- ✅ Si no hay datos: mensaje "No hay..."

---

## 🎯 Prueba 6: Permisos (Opcional - Requiere 2 usuarios)

**Configuración:**
- Usuario A crea worklog en tarjeta X
- Usuario B tiene acceso a la misma tarjeta

**Pasos (como Usuario B):**
1. Abrir tarjeta X
2. Ver worklogs

**Resultado esperado:**
- ✅ Ve el worklog de Usuario A
- ❌ NO tiene botones de editar/eliminar en worklog de A
- ✅ Puede crear su propio worklog
- ✅ SU worklog SÍ tiene botones de editar/eliminar

---

## ✅ Checklist de Verificación Rápida

- [ ] ✅ Crear worklog → Aparece en lista
- [ ] ✅ Editar worklog → Se actualiza
- [ ] ✅ Eliminar worklog → Desaparece
- [ ] ❌ Validación hours < 0.25 → Rechaza
- [ ] ❌ Validación fecha futura → Rechaza
- [ ] ✅ Total de horas calcula correctamente
- [ ] ✅ Página "Mis Horas" carga datos
- [ ] ✅ Cambiar semana recarga datos
- [ ] ✅ Botones solo en worklogs propios
- [ ] ✅ Mensajes de éxito/error aparecen

---

## 🐛 Problemas Comunes

### Error: "Error cargando registros de horas"
**Causa:** Backend no está corriendo o JWT expirado  
**Solución:** 
1. Verificar backend en http://127.0.0.1:8000
2. Hacer logout y login de nuevo

### Error: "No tienes acceso a esta tarjeta"
**Causa:** Usuario no es owner ni miembro del board  
**Solución:** Usar una tarjeta de un tablero propio

### No aparece la sección de worklogs
**Causa:** Estás creando tarjeta nueva (no editando existente)  
**Solución:** Primero guarda la tarjeta, luego ábrela para editar

### Botones de editar/eliminar no aparecen
**Causa:** El worklog es de otro usuario  
**Solución:** Normal, solo puedes editar/eliminar tus propios worklogs

---

## 📊 Endpoints para Testing Manual (Postman/curl)

### Crear Worklog
```bash
POST http://127.0.0.1:8000/worklogs/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "card_id": 1,
  "date": "2026-01-13",
  "hours": 2.5,
  "note": "Testing worklogs"
}
```

### Listar Worklogs de Tarjeta
```bash
GET http://127.0.0.1:8000/worklogs/card/1
Authorization: Bearer {TOKEN}
```

### Mis Horas Semanales
```bash
GET http://127.0.0.1:8000/worklogs/me/week?week=2026-W02
Authorization: Bearer {TOKEN}
```

### Editar Worklog
```bash
PUT http://127.0.0.1:8000/worklogs/1
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "hours": 3.0,
  "note": "Updated note"
}
```

### Eliminar Worklog
```bash
DELETE http://127.0.0.1:8000/worklogs/1
Authorization: Bearer {TOKEN}
```

---

## ✨ Resultado Esperado Final

Al completar todas las pruebas:
- ✅ Módulo worklogs funcionando al 100%
- ✅ CRUD completo operativo
- ✅ Validaciones funcionando
- ✅ Permisos correctos
- ✅ UX pulida con mensajes claros
- ✅ Integración perfecta con el Kanban existente

**Estado:** ✅ LISTO PARA PRODUCCIÓN

---

**Fecha:** 2026-01-13  
**Tiempo de prueba:** 5-10 minutos  
**Cobertura:** Funcionalidad completa

