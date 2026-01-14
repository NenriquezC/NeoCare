# 🌐 Guía de Tests E2E (End-to-End) - NeoCare

## 📋 Descripción

Los tests E2E verifican el funcionamiento completo del sistema desde la perspectiva del usuario, incluyendo:
- **Tests de API**: Verifican los endpoints del backend directamente
- **Tests de UI**: Verifican la interfaz de usuario usando Playwright

---

## ⚙️ Requisitos Previos

### 1. Dependencias de Python

```bash
# Instalar dependencias adicionales para E2E
pip install requests playwright pytest-playwright

# Instalar browsers de Playwright
playwright install chromium
```

### 2. Servicios en Ejecución

Los tests E2E requieren que **AMBOS** servicios estén corriendo:

#### Backend (Puerto 8000)
```bash
cd backend
uvicorn app.main:app --reload
```

#### Frontend (Puerto 5173)
```bash
cd frontend_t
npm run dev
```

---

## 🧪 Tests Disponibles

### Tests de API (15 tests)

Estos tests NO requieren el frontend, solo el backend:

1. **Boards**
   - ✅ `test_api_get_boards` - Obtener tableros del usuario

2. **Lists**
   - ✅ `test_api_get_lists` - Obtener listas de un tablero

3. **Cards (CRUD completo)**
   - ✅ `test_api_create_card` - Crear tarjeta
   - ✅ `test_api_list_cards` - Listar tarjetas
   - ✅ `test_api_get_card_detail` - Obtener detalle de tarjeta
   - ✅ `test_api_update_card_patch` - Actualizar parcialmente (PATCH)
   - ✅ `test_api_update_card_put` - Actualizar completamente (PUT)
   - ✅ `test_api_move_card` - Mover tarjeta
   - ✅ `test_api_delete_card` - Eliminar tarjeta

4. **Worklogs**
   - ✅ `test_api_create_worklog` - Registrar horas
   - ✅ `test_e2e_worklogs_complete_flow` - Flujo completo de worklogs

### Tests de UI (3 tests)

Estos tests requieren TANTO backend COMO frontend:

1. **Login**
   - ✅ `test_ui_login_exitoso` - Login correcto muestra tablero
   - ✅ `test_ui_login_fallido` - Login incorrecto muestra error

2. **Worklogs UI**
   - ✅ `test_ui_worklogs_page` - Página de Mis Horas funcional

---

## 🚀 Ejecución de Tests

### Opción 1: Ejecutar SOLO Tests de API (Recomendado)

```bash
# Asegúrate de que el backend esté corriendo
cd backend
uvicorn app.main:app --reload &

# En otra terminal, ejecutar tests de API
cd backend
python -m pytest tests/e2e/test_e2e.py -v -k "test_api"
```

### Opción 2: Ejecutar Tests de UI

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend_t
npm run dev

# Terminal 3: Tests
cd backend
python -m pytest tests/e2e/test_e2e.py -v -k "test_ui"
```

### Opción 3: Ejecutar TODOS los tests E2E

```bash
# Asegúrate de que AMBOS servicios estén corriendo
# Luego ejecuta:
cd backend
python -m pytest tests/e2e/ -v
```

---

## 📊 Configuración de Variables de Entorno

Los tests E2E leen las siguientes variables de entorno:

```bash
# URLs de los servicios (valores por defecto)
export BACKEND_URL="http://127.0.0.1:8000"
export FRONTEND_URL="http://localhost:5173"
```

Si tus servicios corren en puertos diferentes, configura estas variables antes de ejecutar los tests.

---

## 🔍 Detalles de los Tests

### Test E2E Completo de Worklogs

El test `test_e2e_worklogs_complete_flow` realiza un flujo completo:

1. ✅ **Crear tarjeta** para asociar las horas
2. ✅ **Añadir horas** (3.5h inicialmente)
3. ✅ **Listar horas** de la tarjeta
4. ✅ **Editar horas** (actualizar a 5.0h)
5. ✅ **Ver en "Mis Horas"** (semana actual)
6. ✅ **Eliminar horas**
7. ✅ **Verificar eliminación**

Este test valida todo el ciclo de vida de un worklog.

---

## 🐛 Solución de Problemas

### Error: "Connection refused" o timeout

**Causa**: El backend/frontend no está corriendo  
**Solución**: Inicia los servicios necesarios

```bash
# Verificar que el backend responde
curl http://127.0.0.1:8000/

# Verificar que el frontend responde
curl http://localhost:5173/
```

### Error: "playwright not found"

**Causa**: Playwright no está instalado  
**Solución**:

```bash
pip install playwright pytest-playwright
playwright install chromium
```

### Error: "Email ya registrado"

**Causa**: El test anterior dejó datos en la BD  
**Solución**: Los tests e2e usan emails únicos con UUID, esto no debería pasar. Si ocurre, reinicia el backend.

### Tests de UI fallan pero API funciona

**Causa**: El frontend no está corriendo o los selectores cambiaron  
**Solución**: 
1. Verifica que el frontend esté en http://localhost:5173
2. Revisa los selectores CSS en el código del test

---

## 📝 Comando Rápido (Solo API)

Si solo quieres verificar que la API funciona end-to-end SIN iniciar el frontend:

```bash
# En una terminal: iniciar backend
cd C:\Desarrollo\github\NeoCare\backend
uvicorn app.main:app --reload

# En otra terminal: ejecutar tests de API
cd C:\Desarrollo\github\NeoCare\backend
python -m pytest tests/e2e/test_e2e.py -v -k "test_api" --tb=short
```

---

## ✅ Validación Rápida

Para verificar que los servicios están listos para E2E:

```bash
# 1. Verificar backend
curl http://127.0.0.1:8000/
# Debería responder: {"message":"NeoCare API is running"}

# 2. Verificar frontend (opcional, solo para tests UI)
curl http://localhost:5173/
# Debería responder con HTML del frontend

# 3. Ejecutar un test simple
cd backend
python -m pytest tests/e2e/test_e2e.py::test_api_get_boards -v
```

---

## 🎯 Estado Actual

### Tests de API
- **Estado**: ✅ Listos para ejecutar
- **Requisitos**: Solo backend corriendo
- **Cobertura**: 11 tests de API

### Tests de UI  
- **Estado**: ⚠️ Requieren configuración adicional
- **Requisitos**: Backend + Frontend + Playwright
- **Cobertura**: 3 tests de UI

---

## 📚 Documentación Relacionada

- [Playwright Documentation](https://playwright.dev/python/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 🔄 Integración Continua (CI/CD)

Para ejecutar en CI/CD, usa este workflow:

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install requests playwright pytest-playwright
          playwright install chromium
      
      - name: Start Backend
        run: |
          cd backend
          uvicorn app.main:app &
          sleep 5
      
      - name: Run E2E API Tests
        run: |
          cd backend
          python -m pytest tests/e2e/ -v -k "test_api"
```

---

**Nota**: Los tests E2E son diferentes a los tests unitarios. Mientras que los tests unitarios se ejecutan con una base de datos SQLite en memoria, los tests E2E se ejecutan contra la aplicación real corriendo en modo desarrollo, usando la base de datos PostgreSQL configurada.

