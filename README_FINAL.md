# 📘 NeoCare Health - Kanban + Timesheets - README COMPLETO

> Sistema de gestión de proyectos tipo Kanban con registro de horas integrado

[![FastAPI](https://img.shields.io/badge/FastAPI-0.123-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/)

---

## 📋 Descripción

NeoCare es una aplicación web completa para gestión de proyectos que combina:

✅ **Tableros Kanban** con drag & drop fluido  
✅ **Registro de horas** por tarjeta  
✅ **Informes semanales** automatizados  
✅ **Labels y checklists** para organización  
✅ **Autenticación JWT** segura  
✅ **API REST** robusta y documentada

---

## 🚀 Quick Start

### Requisitos Previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu DATABASE_URL y SECRET_KEY

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

Backend corriendo en: http://localhost:8000

### 2. Frontend

```bash
cd frontend_t

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Verificar VITE_API_URL=http://localhost:8000

# Iniciar desarrollo
npm run dev
```

Frontend corriendo en: http://localhost:5173

---

## 📡 Endpoints Principales

- `POST /auth/register` - Registro
- `POST /auth/login` - Login
- `GET /boards/` - Listar tableros
- `GET /cards/?board_id={id}` - Tarjetas
- `PUT /cards/{id}/move` - Drag & drop
- `POST /worklogs/` - Registrar horas
- `GET /report/{id}/summary` - Informe semanal

📖 **Documentación completa:** http://localhost:8000/docs

---

## 🧪 Testing

```bash
# Backend - 85 tests unitarios
cd backend
python -m pytest -v

# Excluir tests UI
python -m pytest -k "not test_ui"

# Postman Collection
newman run NeoCare_Postman_Collection_Updated.json
```

**Resultados:** 85/85 tests ✅ (100%)

---

## 🌐 Despliegue

📋 **Guía completa:** [DEPLOYMENT.md](DEPLOYMENT.md)

**Backend** → Render  
**Frontend** → Vercel  
**BD** → Railway/Neon

---

## 🎬 Demo

📜 **Guion completo:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

**URL:** https://neocare-frontend.vercel.app  
**Usuario:** demo@neocare.com / Demo123!

---

## 🛠️ Stack Tecnológico

**Backend:** FastAPI 0.123 | PostgreSQL 17 | SQLAlchemy 2.0 | JWT  
**Frontend:** React 19 | TypeScript 5 | Vite 7 | Tailwind CSS 3  
**Testing:** pytest 9.0 | Postman | Playwright

---

## 📂 Estructura

```
NeoCare/
├── backend/              # FastAPI + PostgreSQL
│   ├── app/
│   │   ├── auth/        # JWT
│   │   ├── boards/      # Tableros
│   │   ├── cards/       # Tarjetas + labels + subtasks
│   │   ├── worklogs/    # Horas
│   │   └── report/      # Informes
│   └── tests/           # 85 tests
│
└── frontend_t/          # React + TypeScript
    └── src/
        ├── pages/       # Login, Board, Worklogs, Reports
        └── components/  # Kanban, Cards, Labels
```

---

## 🔗 Documentación Adicional

- 📚 [Despliegue](DEPLOYMENT.md)
- 🎬 [Demo Script](DEMO_SCRIPT.md)  
- 📮 [Colección Postman](NeoCare_Postman_Collection_Updated.json)
- 📊 [Semana 2](README_Semana_2.md) | [Semana 3](README_Semana_3.md) | [Semana 4](README_Semana_4.md)

---

**Estado:** ✅ Listo para producción | **Licencia:** Uso educativo
