# 🎬 Guion Demo Final - NeoCare Health
## Duración: 10-12 minutos

---

## 📋 Preparación Previa

**Datos de Demo:**
- Usuario: `demo@neocare.com` / Password: `Demo123!`
- Tablero: "Proyecto NeoCare Demo"
- 5-8 tarjetas distribuidas en listas
- 10-15 registros de horas de la semana actual

**URLs:**
- Frontend: https://neocare-frontend.vercel.app
- Backend: https://neocare-backend.onrender.com

**Checklist Técnico:**
- [ ] Backend desplegado y funcionando
- [ ] Frontend desplegado y funcionando
- [ ] Datos de demo cargados
- [ ] Internet estable
- [ ] Navegador en pantalla completa
- [ ] Caché limpiada

---

## 🎯 Estructura de la Presentación

### **0. INTRODUCCIÓN** (1 min)
**Quién habla:** Coordinador

```
Buenos días/tardes. Somos el equipo [NOMBRE] y les presentamos 
NeoCare: una herramienta de gestión de proyectos tipo Kanban 
integrada con registro de horas, desarrollada específicamente 
para las necesidades de NeoCare Health.

Nuestro equipo está compuesto por:
- [Nombre] - Coordinador
- [Nombre] - Frontend
- [Nombre] - Backend  
- [Nombre] - Documentador

Durante 6 semanas desarrollamos esta solución completa usando 
React, FastAPI y PostgreSQL.

Hoy les mostraremos las funcionalidades principales en acción.
```

---

### **1. LOGIN Y AUTENTICACIÓN** (1 min)
**Quién habla:** Frontend

**Acciones:**
1. Abrir URL del frontend
2. Mostrar pantalla de login
3. Ingresar credenciales: `demo@neocare.com` / `Demo123!`
4. Click en "Iniciar Sesión"

**Narración:**
```
Comenzamos con el sistema de autenticación seguro basado en JWT.
Cada usuario tiene sus propias credenciales y acceso protegido.

[Escribir email y password]

Una vez autenticados, el token JWT se guarda localmente y nos 
permite acceder a todas las funcionalidades de forma segura.
```

---

### **2. TABLERO KANBAN** (1.5 min)
**Quién habla:** Frontend

**Acciones:**
1. Mostrar vista general del tablero
2. Señalar las 3 listas: "Por hacer", "En curso", "Hecho"
3. Mostrar las tarjetas existentes
4. Destacar labels de colores

**Narración:**
```
Este es nuestro tablero principal estilo Kanban. 
Tenemos 3 listas que representan el flujo de trabajo:
- Por hacer: tareas pendientes
- En curso: trabajo activo
- Hecho: tareas completadas

Cada tarjeta tiene:
- Título y descripción
- Labels de colores para categorización
- Checklist para subtareas
- Responsable asignado
- Fecha de vencimiento
```

---

### **3. CREAR TARJETA** (1.5 min)
**Quién habla:** Frontend

**Acciones:**
1. Click en "+ Nueva Tarjeta" en "Por hacer"
2. Llenar formulario:
   - Título: "Implementar módulo de reportes"
   - Descripción: "Crear visualización de estadísticas"
   - Fecha: Seleccionar fecha futura
3. Guardar
4. Mostrar tarjeta creada

**Narración:**
```
Crear una nueva tarjeta es simple e intuitivo.

[Llenar formulario]

Título: "Implementar módulo de reportes"
Descripción: breve explicación de la tarea
Fecha de vencimiento para tracking

Y la tarjeta aparece inmediatamente en la lista.
```

---

### **4. DRAG & DROP** (1 min)
**Quién habla:** Frontend

**Acciones:**
1. Arrastrar una tarjeta de "Por hacer" a "En curso"
2. Arrastrar otra tarjeta dentro de "En curso" para reordenar
3. Mover una tarjeta a "Hecho"

**Narración:**
```
Una de las funcionalidades clave es el drag and drop fluido.

[Arrastrar tarjeta]

Podemos mover tarjetas entre listas para actualizar su estado,
y también reordenarlas dentro de la misma lista para priorizar.

Todos los cambios se guardan automáticamente en tiempo real.
```

---

### **5. EDITAR TARJETA + LABELS + CHECKLIST** (2 min)
**Quién habla:** Frontend

**Acciones:**
1. Click en una tarjeta para abrir modal
2. Mostrar detalles completos
3. Añadir un label: "Urgente" (rojo)
4. Crear subtarea en checklist: "Diseñar interfaz"
5. Marcar subtarea como completada
6. Guardar cambios

**Narración:**
```
Al hacer click en cualquier tarjeta, accedemos a los detalles completos.

Podemos añadir labels de colores para categorizar visualmente:
[Añadir label "Urgente" en rojo]

Y crear checklists para dividir la tarea en subtareas:
[Añadir "Diseñar interfaz"]

Conforme avanzamos, marcamos las subtareas completadas.
[Check ✓]

El progreso se visualiza con una barra de porcentaje.
```

---

### **6. REGISTRO DE HORAS** (1.5 min)
**Quién habla:** Backend/Frontend

**Acciones:**
1. Dentro de la tarjeta, ir a sección de horas
2. Click en "Registrar Horas"
3. Ingresar:
   - Fecha: Hoy
   - Horas: 4.5
   - Nota: "Desarrollo del módulo principal"
4. Guardar
5. Mostrar registro en la lista

**Narración:**
```
Una característica fundamental es el registro de horas trabajadas.

Desde cualquier tarjeta podemos registrar tiempo:
[Llenar formulario]

Fecha: hoy
Horas: 4.5 horas
Nota opcional: "Desarrollo del módulo principal"

Esto nos permite tener un tracking preciso del tiempo invertido 
en cada tarea para análisis y facturación.
```

---

### **7. MIS HORAS** (1 min)
**Quién habla:** Backend

**Acciones:**
1. Navegar a "Mis Horas" en el menú
2. Mostrar vista semanal con todos los registros
3. Señalar totales por día
4. Destacar tarjetas asociadas

**Narración:**
```
En la vista "Mis Horas" tenemos un resumen personal de la semana.

[Señalar tabla]

Vemos todos nuestros registros de tiempo:
- Fecha
- Tarjeta asociada  
- Horas trabajadas
- Notas

Con totales diarios y semanales para control personal.
```

---

### **8. INFORME SEMANAL** (1.5 min)
**Quién habla:** Backend

**Acciones:**
1. Navegar a "Informes"
2. Seleccionar semana actual
3. Mostrar gráficos:
   - Resumen semanal
   - Horas por usuario
   - Horas por tarjeta
4. Explicar métricas

**Narración:**
```
Para la gestión de proyectos, tenemos informes semanales completos.

[Mostrar dashboard]

Selector de semana para análisis histórico.

Métricas clave:
- Total de horas trabajadas en el proyecto
- Tarjetas completadas vs pendientes  
- Distribución de horas por usuario (para balance de carga)
- Ranking de tarjetas por tiempo invertido

Esto permite a los managers tener visibilidad completa del progreso.
```

---

### **9. ARQUITECTURA TÉCNICA** (1 min)
**Quién habla:** Coordinador/Backend

**Mostrar (opcional: diagrama en slide):**

**Narración:**
```
Desde el punto de vista técnico, NeoCare está construido con:

FRONTEND:
- React 19 con TypeScript para seguridad de tipos
- Vite para build optimizado
- Tailwind CSS para diseño responsive
- React DnD para drag and drop

BACKEND:
- FastAPI con Python para alta performance
- PostgreSQL como base de datos relacional
- SQLAlchemy ORM para manejo de datos
- JWT para autenticación segura
- Alembic para migraciones de BD

DESPLIEGUE:
- Backend en Render
- Frontend en Vercel  
- Base de datos PostgreSQL en Railway/Neon

Todo con CI/CD automático desde GitHub.
```

---

### **10. TESTING Y CALIDAD** (30 seg)
**Quién habla:** Coordinador

**Narración:**
```
En cuanto a calidad y testing:

- 85 tests unitarios (100% de éxito)
- Tests de integración E2E
- Colección Postman con 18 requests automatizados
- Validaciones exhaustivas en frontend y backend
- Manejo de errores robusto
- Base de datos con foreign keys CASCADE para integridad

Todo documentado en nuestro repositorio de GitHub.
```

---

### **11. CIERRE** (1 min)
**Quién habla:** Coordinador

**Narración:**
```
En resumen, NeoCare ofrece:

✓ Gestión visual de tareas con Kanban
✓ Drag & drop intuitivo
✓ Registro preciso de horas trabajadas  
✓ Informes semanales automáticos
✓ Categorización con labels
✓ Checklists para subtareas
✓ Autenticación segura
✓ Arquitectura escalable y moderna

Todo desarrollado en 6 semanas con metodología ágil, 
completamente desplegado y listo para producción.

Aprendizajes clave del equipo:
- Integración frontend-backend
- Gestión de estado compleja (drag & drop)
- Optimización de queries SQL
- Despliegue en entornos cloud
- Trabajo colaborativo con Git

¿Alguna pregunta?

Muchas gracias por su atención.
```

---

## 📊 Distribución de Tiempo

| Sección | Tiempo | Responsable |
|---------|--------|-------------|
| Introducción | 1:00 | Coordinador |
| Login | 1:00 | Frontend |
| Tablero | 1:30 | Frontend |
| Crear tarjeta | 1:30 | Frontend |
| Drag & Drop | 1:00 | Frontend |
| Editar + Labels | 2:00 | Frontend |
| Registro horas | 1:30 | Backend/Frontend |
| Mis Horas | 1:00 | Backend |
| Informes | 1:30 | Backend |
| Arquitectura | 1:00 | Coordinador |
| Testing | 0:30 | Coordinador |
| Cierre | 1:00 | Coordinador |
| **TOTAL** | **13:30** | |

*Ajustar según timing real, objetivo 10-12 min*

---

## ✅ Checklist Pre-Demo

### 1 Día Antes
- [ ] Ensayo completo (cronometrado)
- [ ] Verificar URLs funcionando
- [ ] Datos de demo cargados
- [ ] Screenshots de respaldo preparados
- [ ] Roles asignados claramente

### El Día
- [ ] Llegar 10 min antes
- [ ] Probar conexión internet
- [ ] Limpiar caché del navegador
- [ ] Cerrar pestañas innecesarias
- [ ] Modo presentación (pantalla completa)
- [ ] Silenciar notificaciones

### Plan B (Si falla internet)
- [ ] Video grabado de la demo
- [ ] Screenshots de cada paso
- [ ] Localhost funcionando como backup

---

## 🎯 Consejos para la Presentación

1. **Hablar claro y pausado**: No apresurarse
2. **Señalar con cursor**: Hacer obvio dónde mirar
3. **Explicar antes de hacer**: "Ahora voy a crear una tarjeta"
4. **No disculparse por bugs menores**: Continuar con confianza
5. **Manejar errores con calma**: Tener plan B
6. **Sonreír**: Transmitir confianza en el producto
7. **Tiempo para preguntas**: 2-3 min al final

---

## 🚨 Troubleshooting en Vivo

| Problema | Solución |
|----------|----------|
| Backend no responde | Mencionar "cold start" de Render (30s) |
| Drag & drop falla | Recargar página F5 |
| No carga datos | Verificar conexión, mostrar screenshots |
| Modal no abre | Usar otra tarjeta |
| Internet falla | Cambiar a video/localhost |

---

**Última revisión:** Antes de la presentación
**Responsable:** Coordinador
**Backup:** Todo el equipo conoce el flujo completo
