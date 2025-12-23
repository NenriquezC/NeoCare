🏥 NeoCare Health — Documentación del Proyecto
NeoCare Health — Documentación del Proyecto

Este repositorio contiene el desarrollo del proyecto NeoCare Health, realizado por el equipo Alpha. El objetivo es construir una plataforma enfocada en la gestión de pacientes, datos médicos y acceso seguro mediante un backend robusto con FastAPI y autenticación JWT.

1. Información del Proyecto
Equipo: Alpha

Rol del documentador: Pendiente

Tecnologías usadas:

Frontend
React + Vite

Tailwind CSS

Axios

Backend
Python 3.12

FastAPI

SQLAlchemy

JWT (Python-Jose)

Passlib (hashing)

Base de datos
PostgreSQL

Testing
Postman

PyTest

Playwright

Visual Studio / pruebas unitarias

2. Estructura del Proyecto
/frontend /backend │ main.py │ database.py │ config.py │ models.py │ ├── auth/ │ routes.py │ schemas.py │ utils.py │ └── boards/ routes.py schemas.py /docs /tests README.md

3. Ejecución del Frontend
    Entrar a la carpeta:

    cd frontend


    Instalar dependencias:

    npm install


    Iniciar entorno de desarrollo:

    npm run dev
El proyecto se abre en: http://localhost:3000

4. Ejecución del Backend (FastAPI)
      Entrar a la carpeta:

      cd backend


      Crear entorno virtual (recomendado):

      python -m venv venv
      source venv/bin/activate   # Linux/Mac
      venv\Scripts\activate      # Windows


      Instalar dependencias:

      pip install -r requirements.txt


      Crear archivo .env en la carpeta /backend:

      DATABASE_URL=postgresql://usuario:password@localhost:5432/neocare
      SECRET_KEY=clave_secreta_para_jwt
      ACCESS_TOKEN_EXPIRE_MINUTES=60


      Iniciar el backend:

      uvicorn app.main:app --reload
Servidor disponible en: http://127.0.0.1:8000

Documentación interactiva automática: http://127.0.0.1:8000/docs

5. Configuración de PostgreSQL
      Instalar PostgreSQL

      Crear base de datos:

      CREATE DATABASE neocare;


      Asegurar que usuario/contraseña coinciden con .env

      DATABASE_URL=postgresql://usuario:password@localhost:5432/neocare


      FastAPI creará las tablas automáticamente al iniciar.
6. Testing
API testing con Postman
Incluye pruebas de:

Registro

Login

Generación y validación de JWT

Acceso protegido (/boards)

Los JSON y capturas estarán en: /docs/postman/

Testing unitario – PyTest
Ejemplo:

pytest -v

Testing End-To-End – Playwright
pytest -v

7. Documentación adicional
📁 Actas semanales → /docs/actas/ 📁 Postman collections → /docs/postman/ 📁 Guías técnicas → /docs/manuales/

8. Equipo Alpha
Desarrolladores:

Tester:

Scrum Master:

Documentador:

9. Objetivo Semana 1
Configuración del entorno

Probar API, UI y pruebas E2E

Crear base del README

Preparación del acta y demo


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