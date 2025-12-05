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