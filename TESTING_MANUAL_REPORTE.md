# Guía de Testing Manual - Módulo Informe Semanal

## Prerequisitos

1. Backend arrancado en `http://127.0.0.1:8000`
2. Frontend arrancado en `http://localhost:5173` (o puerto configurado)
3. Base de datos con datos de prueba:
   - Al menos 1 tablero
   - Al menos 3 tarjetas en diferentes listas
   - Al menos 2 registros de tiempo (worklogs)
   - Al menos 1 usuario adicional (para probar membresías)

## Casos de Prueba

### 1. Acceso al Reporte

#### 1.1 Usuario propietario del tablero
**Pasos:**
1. Login como usuario que creó el tablero
2. Navegar a `/report/{boardId}` donde `boardId` es un tablero propio
3. **Resultado esperado:** ✅ Se carga el reporte sin errores

#### 1.2 Usuario miembro del tablero
**Pasos:**
1. Agregar un usuario como miembro del tablero (desde admin/UI)
2. Login como ese usuario
3. Navegar a `/report/{boardId}`
4. **Resultado esperado:** ✅ Se carga el reporte sin errores

#### 1.3 Usuario sin acceso al tablero
**Pasos:**
1. Login como usuario NO propietario NI miembro
2. Navegar a `/report/{boardId}` de un tablero ajeno
3. **Resultado esperado:** ❌ Error 403 "No tienes acceso a este tablero"

### 2. Selector de Semana

#### 2.1 Semana actual por defecto
**Pasos:**
1. Abrir la página de reporte
2. Observar el valor inicial del selector de semana
3. **Resultado esperado:** ✅ Muestra la semana ISO actual (formato YYYY-WXX)

#### 2.2 Cambio de semana
**Pasos:**
1. Cambiar a semana anterior/siguiente usando el selector
2. Observar que los datos se recargan
3. **Resultado esperado:** ✅ Loading indicator + datos actualizados

#### 2.3 Semana sin datos
**Pasos:**
1. Seleccionar una semana muy antigua (sin actividad)
2. **Resultado esperado:** ✅ Resumen muestra contadores en 0 + mensajes "No hubo..."

### 3. Resumen Semanal (SummaryCards)

#### 3.1 Tarjetas completadas
**Preparación:**
- Crear/mover una tarjeta a lista "Hecho" durante la semana seleccionada
- Asegurar que `completed_at` esté en el rango de la semana

**Resultado esperado:**
- ✅ Contador de "Completadas" > 0
- ✅ Aparece en el top 5 con badge verde #ID
- ✅ Título de la tarjeta visible

#### 3.2 Tarjetas nuevas
**Preparación:**
- Crear una tarjeta con `created_at` en la semana seleccionada

**Resultado esperado:**
- ✅ Contador de "Nuevas" > 0
- ✅ Aparece en el top 5 con badge azul #ID

#### 3.3 Tarjetas vencidas
**Preparación:**
- Crear una tarjeta con `due_date` en la semana seleccionada
- Asegurar que NO está en lista "Hecho" y NO tiene `completed_at`

**Resultado esperado:**
- ✅ Contador de "Vencidas" > 0
- ✅ Aparece en el top 5 con badge rojo #ID

#### 3.4 Empty states
**Preparación:**
- Seleccionar una semana sin actividad

**Resultado esperado:**
- ✅ "No hubo tareas completadas esta semana"
- ✅ "No hubo tareas nuevas esta semana"
- ✅ "No hubo tareas vencidas esta semana"

### 4. Horas por Usuario

#### 4.1 Tabla poblada
**Preparación:**
- Crear al menos 2 worklogs en tarjetas del tablero durante la semana

**Resultado esperado:**
- ✅ Tabla muestra filas con:
  - Nombre de usuario
  - Total de horas (formato decimal con 2 decimales)
  - Número de tareas únicas

#### 4.2 Exportar CSV
**Pasos:**
1. Click en botón "Exportar CSV"
2. Abrir el archivo descargado en Excel/LibreOffice

**Resultado esperado:**
- ✅ Archivo descargado: `horas-por-usuario-YYYY-WXX.csv`
- ✅ Columnas: user_id, user_name, total_hours, tasks_count
- ✅ Caracteres especiales (tildes, ñ) se ven correctamente
- ✅ Datos coinciden con la tabla

#### 4.3 Sin datos
**Preparación:**
- Semana sin worklogs

**Resultado esperado:**
- ✅ Mensaje: "No hay registros de horas por usuario para esta semana"
- ✅ Botón CSV deshabilitado (disabled)

### 5. Horas por Tarjeta

#### 5.1 Tabla poblada y ordenada
**Preparación:**
- Crear worklogs en diferentes tarjetas con diferentes horas

**Resultado esperado:**
- ✅ Tabla muestra:
  - Título de tarjeta
  - Responsable (o "—" si es null)
  - Estado (nombre de lista)
  - Total de horas
- ✅ Ordenadas de mayor a menor horas

#### 5.2 Exportar CSV
**Pasos:**
1. Click en botón "Exportar CSV" (nuevo botón)
2. Abrir archivo

**Resultado esperado:**
- ✅ Archivo: `horas-por-tarjeta-YYYY-WXX.csv`
- ✅ Columnas: card_id, title, responsible, status, total_hours
- ✅ Datos correctos

### 6. Validaciones de Semana

#### 6.1 Formato inválido (Backend)
**Pasos:**
1. Hacer petición manual a `/report/{boardId}/summary?week=2026W02` (sin guión)
2. **Resultado esperado:** ❌ HTTP 400 "Formato de semana inválido"

#### 6.2 Semana inexistente
**Pasos:**
1. Hacer petición a `/report/{boardId}/summary?week=2026-W54`
2. **Resultado esperado:** ❌ HTTP 400 "Semana ISO inválida"

### 7. Performance y UX

#### 7.1 Loading states
**Observar:**
- ✅ Aparece mensaje "Cargando reporte…" durante las peticiones
- ✅ Se oculta cuando termina la carga

#### 7.2 Error handling
**Simular:**
- Apagar el backend mientras se carga el reporte

**Resultado esperado:**
- ✅ Mensaje de error descriptivo (no crash)
- ✅ Posibilidad de reintentar

#### 7.3 Responsividad
**Probar en:**
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

**Resultado esperado:**
- ✅ Cards se adaptan (pueden apilarse en mobile)
- ✅ Tablas tienen scroll horizontal si es necesario

### 8. Integración E2E

#### Escenario completo:
1. Crear tablero nuevo
2. Crear 3 listas: "Por hacer", "En curso", "Hecho"
3. Crear 5 tarjetas:
   - 2 en "Por hacer" con fecha de vencimiento esta semana
   - 2 en "En curso"
   - 1 en "Hecho" con `completed_at` esta semana
4. Agregar worklogs a 3 tarjetas
5. Ir al reporte de esta semana

**Resultado esperado:**
- ✅ Completadas: 1
- ✅ Nuevas: 5
- ✅ Vencidas: 2
- ✅ Horas por usuario: datos visibles
- ✅ Horas por tarjeta: 3 filas
- ✅ Exportación CSV funciona para ambas tablas

## Checklist Final

- [ ] Backend arranca sin errores
- [ ] Frontend arranca sin errores
- [ ] Ruta `/report/{boardId}` accesible
- [ ] Selector de semana muestra semana actual
- [ ] Resumen muestra 3 categorías
- [ ] Top 5 items se muestran con badges
- [ ] Empty states funcionan
- [ ] Tabla horas por usuario funciona
- [ ] Tabla horas por tarjeta funciona
- [ ] Ambos botones CSV funcionan
- [ ] Permisos 403 para usuarios sin acceso
- [ ] Validación 400 para semanas inválidas
- [ ] Loading/error states funcionan

---

## Comandos Útiles

### Arrancar Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### Arrancar Frontend
```bash
cd frontend_t
npm run dev
```

### Ver logs Backend
```bash
# En PowerShell del backend, los logs aparecen en consola
```

### Hacer petición manual (PowerShell)
```powershell
# Obtener token
$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method POST -Body (@{username="test@test.com"; password="test123"} | ConvertTo-Json) -ContentType "application/json"
$token = $loginResponse.access_token

# Llamar endpoint
Invoke-RestMethod -Uri "http://127.0.0.1:8000/report/1/summary?week=2026-W02" -Headers @{Authorization="Bearer $token"}
```

---

**Fecha de creación:** 2026-01-13

