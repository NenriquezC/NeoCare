# 🏥 NeoCare Health — Documentación del Proyecto

Este repositorio contiene el desarrollo del proyecto **NeoCare Health**, realizado por el equipo **Alpha**.  
El objetivo es construir una plataforma enfocada en la gestión de pacientes, datos médicos y acceso seguro.


## 1. Información del Proyecto

- **Equipo:** Alpha  
- **Rol del documentador:** 
- **Tecnologías usadas:**  
  - Frontend: React / Vite  
  - Backend: Node.js / Express  
  - Base de datos: PostgreSQL  
  - Testing: Postman, Cypress, Playwright, Visual Studio (unit tests)  


## 2. Estructura del Proyecto
/frontend
/backend
/docs
/tests
README.md


## 3. Ejecución del Frontend

1. Entrar a la carpeta del frontend:

cd frontend

2. Instalar dependencias:

npm install

3. Iniciar entorno de desarrollo:

npm run dev

El proyecto se abre en:
 http://localhost:3000

## 4. Ejecución del Backend

1. Entrar a la carpeta del backend:

cd backend

2. Instalar dependencias:

npm install

3. Configurar archivo.env:

DATABASE_URL=postgres://usuario:password@localhost:5432/neocare
JWT_SECRET=clave_secreta
PORT=3001

4. Iniciar backend:

npm run dev

Backend disponible en:
 http://localhost:3001

## 5. Configuración de PostgreSQL

1. Instalar PostgreSQL

2. Crear la base de datos:

CREATE DATABASE neocare;

3. Verificar usuario y contraseña configurados

C4. onfirmar que coinciden con la variable:

DATABASE_URL=postgres://usuario:password@localhost:5432/neocare

## 6. Testing

# API testing con Postman

Las pruebas incluyen: Login, registro de usuarios y acceso protehido por Token
Se adjuntarán capturas o Json del informe semanal

# Testing unitario- Visual STudio

Test: ShouldReturnUser_WhenIdIsValid
Resultado: Pasó
Notas: Se detectó lentitud en el método GetUser()

# Testing End-To-End- Playwright

pytest -v


## 7. Documentación adicional
Actas semanales: /docs/actas/

Postman collections: /docs/postman/

Guías técnicas: /docs/manuales/

## 8. Equipo Alpha
Desarrolladores:

Tester: 

Scrum Master:

Documentador: 

## 9. Objetivo de la Semana 1
Configuración del entorno

Primeras pruebas: API, UI y E2E

Creación de la base del README

Preparación de acta y guion de mini demo

