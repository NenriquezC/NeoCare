# 🏥 NeoCare Health — Documentación del Proyecto

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)](https://www.postgresql.org/)

**NeoCare Health** es una plataforma de gestión de pacientes y datos médicos desarrollada por el **Equipo Alpha**, con un backend robusto en FastAPI, autenticación JWT y un frontend moderno en React.

---

## 📋 Tabla de Contenidos

1. [Información del Proyecto](#1-información-del-proyecto)
2. [Inicio Rápido](#2-inicio-rápido)
3. [Configuración Inicial](#3-configuración-inicial-del-proyecto)
4. [Configuración de Base de Datos](#4-configuración-de-la-base-de-datos)
5. [Ejecución del Proyecto](#5-ejecución-del-proyecto)
6. [Estructura del Proyecto](#6-estructura-del-proyecto)
7. [Scripts Disponibles](#7-scripts-disponibles)
8. [Endpoints de la API](#8-endpoints-principales-de-la-api)
9. [Solución de Problemas](#9-solución-de-problemas-comunes)
10. [Testing](#10-testing)
11. [Tecnologías](#11-tecnologías-utilizadas)
12. [Variables de Entorno](#12-variables-de-entorno)
13. [Comandos de Referencia](#13-comandos-rápidos-de-referencia)

---

## 1. Información del Proyecto

**Equipo**: Alpha  
**Objetivo**: Plataforma de gestión médica con acceso seguro y gestión de tableros tipo Kanban para organización de tareas.

### Tecnologías Principales

| Componente | Tecnología |
|------------|------------|
| **Backend** | FastAPI, Python 3.12+, SQLAlchemy |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Base de Datos** | PostgreSQL |
| **Autenticación** | JWT (Python-Jose) |
| **Testing** | PyTest, Postman |

---

## 2. Inicio Rápido

### ⚡ Instalación en 3 Pasos

```powershell
# 1. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r backend/requirements.txt
cd frontend_t
npm install
cd ..

# 3. Configurar base de datos y .env (ver sección 4)
# Luego ejecutar:
.\start-all.ps1
```

✅ **Backend**: http://127.0.0.1:8000  
✅ **Frontend**: http://localhost:5173  
📚 **API Docs**: http://127.0.0.1:8000/docs

---

## 3. Configuración Inicial del Proyecto

### 3.1 Requisitos Previos
- **Python 3.12+** instalado
- **Node.js 18+** y npm instalados
- **PostgreSQL** instalado y corriendo
- **Git** (opcional, para control de versiones)

### 3.2 Instalación del Entorno Virtual (IMPORTANTE)

El proyecto utiliza un entorno virtual compartido en la raíz del proyecto:

```bash
# Desde la raíz del proyecto (NeoCare/)
python -m venv .venv
```

**Activar el entorno virtual:**

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

**Instalar todas las dependencias del backend:**

```bash
# Con el entorno virtual activado
pip install -r backend/requirements.txt
```

> ⚠️ **Importante**: Siempre activa el entorno virtual antes de trabajar con el backend.

---

## 4. Configuración de la Base de Datos

### 4.1 Crear la Base de Datos en PostgreSQL

```sql
CREATE DATABASE neocare;
```

### 4.2 Configurar el archivo .env

Crea un archivo `.env` dentro de la carpeta `backend/`:

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/neocare
SECRET_KEY=clave-secreta-super-segura-cambiala-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Reemplaza**:
- `TU_CONTRASEÑA` con tu contraseña de PostgreSQL
- `neocare` con el nombre de tu base de datos
- `SECRET_KEY` con una clave secreta única (usa al menos 32 caracteres aleatorios)

> 💡 **Importante**: El archivo `.env` es donde se configura la base de datos para desarrollo/producción. El sistema carga automáticamente este archivo usando `python-dotenv`.

### 4.3 Bases de Datos: Desarrollo vs Testing

El proyecto usa **dos bases de datos diferentes** dependiendo del contexto:

| Contexto | Base de Datos | Configuración |
|----------|---------------|---------------|
| **Desarrollo/Postman** | PostgreSQL | `backend/.env` → `DATABASE_URL` |
| **Tests Unitarios** | SQLite | Automático vía `tests/conftest.py` |

**¿Por qué SQLite para tests?**
- ✅ Evita problemas de encoding UTF-8 en Windows
- ✅ Tests más rápidos (base de datos en memoria)
- ✅ Aislamiento total entre tests
- ✅ No requiere PostgreSQL corriendo

El cambio entre bases de datos es **automático**:
- Al ejecutar `pytest`, se establece `TESTING=1` y usa SQLite
- Al ejecutar el servidor (`uvicorn`), usa PostgreSQL del `.env`

### 4.4 Solución de Problemas de Encoding (Windows)

Si obtienes el error `UnicodeDecodeError: 'utf-8' codec can't decode byte`, el archivo `backend/app/database.py` ya está configurado para solucionarlo automáticamente con:

- Carga automática del archivo `.env` usando `python-dotenv`
- Forzado de codificación UTF-8 en Windows
- Parámetros de conexión correctos para PostgreSQL
- Detección automática de modo test (SQLite) vs desarrollo (PostgreSQL)

**El sistema funciona así:**
1. Lee el `.env` al iniciar
2. Si `TESTING=1` → usa SQLite (tests)
3. Si no → usa PostgreSQL del `.env` (desarrollo/producción)

---

## 5. Ejecución del Proyecto

### 5.1 Opción 1: Iniciar Todo con un Solo Comando (Recomendado)

Desde la raíz del proyecto:

```powershell
.\start-all.ps1
```

Este script abrirá dos ventanas:
- **Backend** en http://127.0.0.1:8000
- **Frontend** en http://localhost:5173

### 5.2 Opción 2: Iniciar Manualmente

#### Backend

```powershell
cd backend
& ..\\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

✅ Servidor corriendo en: **http://127.0.0.1:8000**  
📚 Documentación API: **http://127.0.0.1:8000/docs**

#### Frontend

```bash
cd frontend_t
npm install  # Solo la primera vez
npm run dev
```

✅ Aplicación corriendo en: **http://localhost:5173**

---

## 6. Estructura del Proyecto

```
NeoCare/
├── .venv/                          # Entorno virtual de Python (compartido)
├── backend/
│   ├── .env                        # Variables de entorno (crear manualmente)
│   ├── app/
│   │   ├── main.py                 # Punto de entrada de FastAPI
│   │   ├── database.py             # Configuración de la BD
│   │   ├── config.py               # Configuración global
│   │   ├── auth/
│   │   │   ├── routes.py           # Rutas de autenticación
│   │   │   ├── schemas.py          # Modelos Pydantic
│   │   │   └── utils.py            # JWT y hashing
│   │   ├── boards/
│   │   │   ├── models.py           # Modelos SQLAlchemy
│   │   │   ├── routes.py           # Endpoints de tableros
│   │   │   └── schemas.py          # Validaciones
│   │   ├── cards/
│   │   │   ├── routes.py           # Endpoints de tarjetas
│   │   │   └── schemas.py
│   │   └── worklogs/
│   │       ├── routes.py           # Endpoints de registros de tiempo
│   │       └── schemas.py
│   ├── tests/                      # Tests unitarios y E2E
│   ├── requirements.txt            # Dependencias Python
│   └── start.ps1                   # Script para iniciar solo backend
├── frontend_t/
│   ├── src/
│   │   ├── pages/                  # Páginas principales
│   │   ├── components/             # Componentes reutilizables
│   │   ├── lib/                    # Utilidades y API
│   │   └── main.tsx                # Punto de entrada React
│   ├── package.json
│   └── vite.config.ts
├── start-all.ps1                   # Script para iniciar todo
└── readme.md                       # Este archivo
```

---

## 7. Scripts Disponibles

### Backend
```bash
# Iniciar servidor de desarrollo
python -m uvicorn app.main:app --reload

# Ejecutar tests
pytest -v

# Crear migraciones (Alembic)
alembic revision --autogenerate -m "descripción"
alembic upgrade head
```

### Frontend
```bash
# Instalar dependencias
npm install

# Servidor de desarrollo
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview
```

---

## 8. Endpoints Principales de la API

### Autenticación
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión (devuelve JWT)

### Tableros (requiere autenticación)
- `GET /boards` - Listar tableros del usuario
- `POST /boards` - Crear nuevo tablero
- `GET /boards/{id}` - Obtener tablero específico
- `PUT /boards/{id}` - Actualizar tablero
- `DELETE /boards/{id}` - Eliminar tablero

### Tarjetas
- `GET /boards/{board_id}/cards` - Listar tarjetas de un tablero
- `POST /cards` - Crear tarjeta
- `PUT /cards/{id}` - Actualizar tarjeta
- `DELETE /cards/{id}` - Eliminar tarjeta

### Worklogs (Registros de Tiempo)
- `GET /worklogs/card/{card_id}` - Listar worklogs de una tarjeta
- `POST /worklogs` - Crear registro de tiempo
- `PUT /worklogs/{id}` - Actualizar worklog
- `DELETE /worklogs/{id}` - Eliminar worklog
- `GET /worklogs/me/week?week=YYYY-Www` - Mis horas por semana

📚 **Documentación completa**: http://127.0.0.1:8000/docs (con backend corriendo)

---

## 9. Solución de Problemas Comunes

### ❌ Error: "uvicorn: no se reconoce como comando"
**Solución**: Asegúrate de activar el entorno virtual antes:
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

### ❌ Error: "vite: no se reconoce como comando"
**Solución**: Instala las dependencias del frontend:
```bash
cd frontend_t
npm install
```

### ❌ Error: "UnicodeDecodeError" en la conexión a PostgreSQL
**Solución**: Ya está configurado en `backend/app/database.py`. Si persiste:
1. Verifica que tu contraseña en `.env` no tenga caracteres especiales sin URL-encodear
2. Asegúrate de que PostgreSQL esté configurado con encoding UTF-8

### ❌ Error: "Could not connect to database"
**Solución**:
1. Verifica que PostgreSQL esté corriendo
2. Confirma que la base de datos `neocare` existe
3. Revisa que usuario/contraseña en `.env` sean correctos
4. Prueba la conexión:
   ```bash
   psql -U postgres -d neocare
   ```

### ❌ Error: "Module not found" en Python
**Solución**: Reinstala las dependencias:
```bash
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

---

## 10. Testing
## 10. Testing

### 10.1 Arquitectura de Testing

El proyecto utiliza **dos bases de datos separadas**:
- **PostgreSQL** para desarrollo y Postman (flujo real de la aplicación)
- **SQLite** para tests unitarios (automático, sin configuración)

Esta separación garantiza:
- ✅ Tests rápidos y sin dependencias externas
- ✅ Sin problemas de encoding en Windows
- ✅ Aislamiento total entre tests
- ✅ Postman prueba el flujo real con PostgreSQL

### 10.2 Testing Unitario con PyTest

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar todos los tests
cd backend
pytest -v

# Tests específicos por módulo
pytest tests/auth/ -v                 # Solo tests de autenticación
pytest tests/boards/ -v               # Solo tests de tableros
pytest tests/cards/ -v                # Solo tests de tarjetas
pytest tests/worklogs/ -v             # Solo tests de worklogs

# Con coverage
pytest --cov=app tests/

# Ignorar tests e2e (requieren Playwright)
pytest tests/ -v --ignore=tests/e2e
```

**Resultado esperado**: Todos los tests deben pasar con SQLite
```
========================== 44 passed, 1 warning in 9.78s ==========================
```

### 10.3 Testing con Postman
Importa las colecciones ubicadas en la raíz del proyecto:
- `NeoCare_Postman_Collection_Updated.json` - Colección actualizada
- `POSTMAN_GUIDE.md` - Guía de uso

**Tests incluidos**:
- ✅ Registro de usuarios
- ✅ Login y generación de JWT
- ✅ Validación de tokens
- ✅ CRUD de tableros (boards)
- ✅ CRUD de tarjetas (cards)
- ✅ Gestión de worklogs

> **Nota**: Postman usa **PostgreSQL** (configurado en `.env`), mientras que pytest usa **SQLite** automáticamente.

### 10.4 Testing End-to-End

```bash
# Requiere Playwright instalado
cd backend
pytest tests/e2e/ -v
```

### 10.5 Configuración de Tests (Información Técnica)

Los tests están configurados en:
- `backend/tests/conftest.py` - Configuración global de pytest
  - Establece `TESTING=1` antes de importar la app
  - Crea fixtures con base de datos SQLite limpia
  - Cada test tiene su propia base de datos aislada

- `backend/app/database.py` - Detección automática de modo
  ```python
  IS_TESTING = os.getenv("TESTING", "0") == "1"
  if IS_TESTING:
      DATABASE_URL = "sqlite:///./test.db"  # Tests
  else:
      DATABASE_URL = os.getenv("DATABASE_URL", ...)  # Desarrollo
  ```

---

## 11. Tecnologías Utilizadas

### Backend
- **FastAPI** 0.128.0 - Framework web moderno y rápido
- **SQLAlchemy** 2.0.45 - ORM para Python
- **PostgreSQL** - Base de datos relacional (desarrollo/producción)
- **SQLite** - Base de datos para tests (automático)
- **Python-dotenv** - Carga de variables de entorno desde `.env`
- **Pydantic** 2.12.5 - Validación de datos
- **Python-Jose** - Manejo de JWT
- **Passlib + Bcrypt** - Hashing de contraseñas
- **Alembic** - Migraciones de BD
- **Uvicorn** - Servidor ASGI
- **Pytest** - Framework de testing

### Frontend
- **React** 18+ - Librería UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Framework CSS
- **React Router** - Navegación
- **Axios** - Cliente HTTP

---

## 12. Variables de Entorno

### Backend (.env)
```bash
# Base de datos
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/neocare

# JWT
SECRET_KEY=clave-super-secreta-minimo-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> 💡 **Tip**: Para generar una SECRET_KEY segura en Python:
> ```python
> import secrets
> print(secrets.token_urlsafe(32))
> ```

---

## 13. Comandos Rápidos de Referencia

### Iniciar el Proyecto Completo
```powershell
# Opción 1: Script automático
.\start-all.ps1

# Opción 2: Manual
# Terminal 1 - Backend
cd backend
& ..\\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend_t
npm run dev
```

### Gestión de Base de Datos
```bash
# Crear migración
cd backend
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history
```

### Desarrollo
```bash
# Ver logs del backend (ya los ves en la terminal)
# Acceder a la BD
psql -U postgres -d neocare

# Limpiar cache de Python
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force  # Windows
```

---

## 14. Contribuir al Proyecto

### Flujo de Trabajo Git
```bash
# 1. Crear rama para nueva feature
git checkout -b feature/nombre-feature

# 2. Hacer cambios y commits
git add .
git commit -m "Descripción clara del cambio"

# 3. Push de la rama
git push origin feature/nombre-feature

# 4. Crear Pull Request en GitHub
```

### Convenciones de Código

**Python (Backend)**:
- Seguir PEP 8
- Usar type hints
- Documentar funciones con docstrings
- Nombres en snake_case

**TypeScript (Frontend)**:
- Seguir guía de estilo de Airbnb
- Usar interfaces para tipos
- Componentes en PascalCase
- Funciones/variables en camelCase

---

## 15. Documentación Adicional

📁 **Archivos de Referencia**:
- `openapi.json` - Especificación OpenAPI de la API
- `POSTMAN_GUIDE.md` - Guía detallada de Postman
- `backend/alembic.ini` - Configuración de Alembic
- `frontend_t/vite.config.ts` - Configuración de Vite

📚 **Recursos**:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 16. Equipo Alpha

**Desarrolladores**: [Nombres]  
**Tester**: [Nombre]  
**Scrum Master**: [Nombre]  
**Documentador**: [Nombre]

---

## 17. Licencia

Este proyecto es parte del curso [Nombre del Curso] en [Institución].  
Todos los derechos reservados © 2026 Equipo Alpha.

---

## 📞 Soporte

Si encuentras problemas:
1. ✅ Revisa la sección "Solución de Problemas Comunes"
2. ✅ Verifica que todos los servicios estén corriendo (PostgreSQL, Backend, Frontend)
3. ✅ Consulta los logs en la terminal
4. ✅ Revisa la documentación en http://127.0.0.1:8000/docs

---

**Última actualización**: Enero 2026  
**Versión del README**: 2.0


SEMANA3: BACKEND
🧠 NeoCare Kanban – Backend

Backend del proyecto NeoCare Kanban, una aplicación de gestión de tareas tipo Kanban desarrollada con FastAPI, SQLAlchemy y PostgreSQL, con autenticación basada en JWT y testing automatizado.

Este backend está diseñado como una API REST segura, testeada y escalable, preparada para integrarse con un frontend moderno (React).

🚀 Stack tecnológico

Python 3.12

FastAPI

SQLAlchemy

PostgreSQL

JWT (JSON Web Tokens)

Pytest (testing)

Uvicorn (ASGI server)

📁 Estructura del proyecto
backend/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py            # Configuración central (env, JWT, DB)
│   ├── database.py          # Conexión y sesión SQLAlchemy
│   │
│   ├── auth/                # Autenticación y seguridad
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── utils.py
│   │
│   ├── boards/              # Tableros Kanban
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   └── cards/               # Tarjetas Kanban
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
│
├── tests/                   # Testing automatizado
│   ├── auth/
│   ├── boards/
│   ├── cards/
│   ├── e2e/
│   └── test_main.py
│
├── pytest.ini
├── requirements.txt
└── README.md

🔐 Autenticación (JWT)

El sistema utiliza JWT (JSON Web Tokens) para proteger los endpoints.

Endpoints principales:

POST /auth/register → Registro de usuario

POST /auth/login → Login y obtención de token

Uso del token:
Authorization: Bearer <access_token>


Todas las rutas protegidas validan:

Token válido

Usuario autenticado

Permisos sobre el recurso

🗂️ Funcionalidades principales
👤 Usuarios

Registro

Login

Autenticación segura con JWT

📋 Tableros (Boards)

Crear tablero

Listar tableros del usuario

Control de acceso por propietario

🗃️ Tarjetas (Cards)

Crear, editar y eliminar tarjetas

Mover tarjetas entre columnas (drag & drop)

Control de orden y posiciones

Validación de datos

Seguridad por tablero

El backend es la autoridad del orden, no el frontend.

▶️ Ejecutar el backend en local
1️⃣ Crear y activar entorno virtual
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

2️⃣ Instalar dependencias
pip install -r requirements.txt

3️⃣ Levantar el servidor
uvicorn app.main:app --reload


📍 Backend disponible en:

http://127.0.0.1:8000


📘 Documentación automática (Swagger):

http://127.0.0.1:8000/docs

🧪 Testing

El backend cuenta con testing automatizado completo.

Tipos de pruebas:

Tests unitarios

Tests de integración (API)

Tests End-to-End (definidos, no ejecutados por defecto)

▶️ Ejecutar tests de backend (recomendado)
pytest -k "not e2e"


✔️ Resultado esperado:

43 passed, 3 deselected

⚠️ Tests E2E

Los tests E2E requieren:

Frontend levantado

Navegador (Playwright)

Por eso no se ejecutan por defecto.
Esto es una decisión técnica consciente y profesional.

🧠 Decisiones técnicas clave

Separación clara entre backend y frontend

Backend como autoridad de seguridad y lógica

Validaciones en Pydantic + SQLAlchemy

JWT como mecanismo de autenticación estándar

Testing como parte del contrato del sistema

📌 Estado del proyecto

✅ Backend completo y funcional

✅ Seguridad implementada

✅ Testing automatizado

🔜 Integración frontend

🔜 CI/CD
######3##############################################################################################################################
# 🏥 NeoCare — Gestión de Proyectos y Registro de Horas

Aplicación web tipo **Kanban profesional** para la gestión de proyectos y el registro de horas trabajadas por usuario.

El proyecto está desarrollado con una **arquitectura moderna full-stack**, separando frontend, backend y base de datos, y se ha construido de forma incremental por **semanas**, siguiendo objetivos claros y verificables.

---

## 🧰 Stack Tecnológico

**Backend**
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (JSON Web Tokens)

**Frontend**
- React
- Vite
- TypeScript

**Otros**
- Git / GitHub
- Pytest (testing)
- JWT para autenticación segura

---

## 🧱 Arquitectura General
- Frontend: SPA (Single Page Application)
- Backend: API REST
- Autenticación: Stateless mediante JWT
- Base de datos: Relacional

---

# 📅 Desarrollo por Semanas

---

## ✅ Semana 1 — Fundamentos y Autenticación

### 🎯 Objetivo
Crear la base del sistema: usuarios, autenticación y comunicación segura entre frontend y backend.

### Backend
- Registro de usuarios
- Login con validación de credenciales
- Hash de contraseñas
- Generación de tokens JWT
- Protección de rutas privadas
- Conexión a PostgreSQL
- Estructura modular del proyecto

**Archivos principales**
backend/app/
├── main.py
├── config.py
├── database.py
├── auth/
│ ├── routes.py
│ ├── schemas.py
│ ├── utils.py

### Frontend
- Pantalla de login
- Envío de credenciales al backend
- Almacenamiento del JWT
- Redirección tras login
- Bloqueo de acceso sin token

### Testing
- Verificación de login end-to-end
- Comprobación de acceso restringido sin JWT
- Flujo completo frontend ↔ backend probado en local

---

## ✅ Semana 2 — Tableros y Tarjetas (Kanban)

### 🎯 Objetivo
Implementar la funcionalidad central del producto: gestión de tableros, listas y tarjetas.

### Backend
- Crear tableros
- Crear listas dentro de un tablero
- Crear, editar y listar tarjetas
- Validación de permisos por usuario
- Respuestas HTTP claras (403 / 404)

**Estructura**
backend/app/
├── boards/
│ ├── models.py
│ ├── routes.py
│ ├── schemas.py
├── cards/
│ ├── models.py
│ ├── routes.py
│ ├── schemas.py


### Frontend
- Visualización del tablero
- Listas como columnas
- Tarjetas movibles
- Edición sin recargar la página
- Sincronización con el backend

### Testing
- Crear tarjeta con datos válidos
- Fallos controlados (título vacío, fecha inválida)
- Edición correcta
- Validación de orden y permisos

---

## ✅ Semana 3 — Control de Versiones y Calidad

### 🎯 Objetivo
Trabajar con un flujo real de desarrollo profesional usando Git y testing consciente.

### Git & Workflow
- Uso de ramas (`master`, `semana_3`)
- Diferencia entre working tree, staging y commit
- Pull y push correctos
- Resolución de conflictos
- Sincronización con cambios de colaboradores

### Testing
- Tests con `pytest`
- Pruebas manuales con frontend real
- Validación de seguridad JWT
- Pruebas sin depender de Postman o Playwright

> Enfoque: entender **qué se prueba, por qué y qué garantiza**.

---

## ✅ Semana 4 — Registro de Horas (Worklogs)

### 🎯 Objetivo
Implementar el sistema de registro de horas trabajadas por tarjeta y por usuario.

### Backend
- Añadir horas a una tarjeta
- Listar horas por tarjeta
- Editar horas (solo autor)
- Eliminar horas (solo autor)
- Consultar “Mis horas” por semana

**Endpoints principales**
POST /worklogs
GET /worklogs/card/{card_id}
GET /worklogs/me/week?week=YYYY-WW
PUT /worklogs/{id}
DELETE /worklogs/{id}

yaml
Copiar código

> El backend devuelve los datos envueltos en un objeto `{ "entries": [...] }`,
lo que requiere que el frontend consuma correctamente la respuesta.

### Frontend
- Formulario de horas dentro de la tarjeta
- Listado inmediato tras añadir horas
- Vista “Mis horas”
- Filtro por semana
- Actualización sin recargar

### Testing
- Persistencia correcta en base de datos
- Seguridad por usuario
- Consulta semanal funcional
- Identificación y corrección de bugs reales sin tocar backend innecesariamente

---

## 🏁 Estado Actual del Proyecto

Al finalizar la semana 4, NeoCare cuenta con:

- Autenticación segura con JWT
- Gestión completa de tableros, listas y tarjetas
- Registro de horas por tarjeta
- Consulta de horas personales por semana
- Arquitectura backend/frontend separada
- Testing funcional y de seguridad
- Flujo Git profesional

---

## 🚀 Próximos Pasos

- Mejora de UX/UI
- Dashboard con estadísticas
- Optimización de consultas
- Testing E2E (Playwright)
- Dockerización y despliegue

---

## 👤 Autor

Proyecto desarrollado como ejercicio práctico de arquitectura full-stack,
seguridad, testing y control de versiones en un entorno realista.