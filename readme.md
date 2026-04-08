# 🏥 NeoCare — Project & Time Management Platform

A full-stack Kanban-style web application for project management and 
time tracking, built with a modern REST API backend and a reactive frontend.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Tests](https://img.shields.io/badge/tests-44%20passed-brightgreen)

---

## 🚀 Overview

NeoCare is a task and time management platform built with a clean 
backend/frontend separation. Users can organize work using Kanban boards, 
manage cards across columns, and log hours per task with weekly summaries.

**My role:** Backend development — API architecture, authentication system, 
data models, and automated testing.

---

## 🧰 Tech Stack

| Layer       | Technologies                                      |
|-------------|---------------------------------------------------|
| Backend     | Python 3.12, FastAPI, SQLAlchemy, Alembic         |
| Auth        | JWT (python-jose), Passlib + Bcrypt               |
| Database    | PostgreSQL (dev/prod), SQLite (testing)           |
| Frontend    | React 18, TypeScript, Vite, Tailwind CSS, Axios  |
| Testing     | Pytest (44 tests), Postman, Playwright (E2E)     |

---

## 📐 Architecture

- **REST API** with modular routing: `auth/`, `boards/`, `cards/`, `worklogs/`
- **Stateless authentication** via JWT — backend is the single authority
- **Dual database strategy**: PostgreSQL for dev, SQLite for isolated testing
- **Pydantic v2** for request/response validation
- **Alembic** for database migrations

---

## 🔐 Authentication Flow
POST /auth/register   → Create user (hashed password)
POST /auth/login      → Returns JWT access token
Authorization: Bearer <token>  → Required for all protected routes

---

## 📋 Core Endpoints

### Boards
GET  /boards                        → List user boards
GET  /boards/{board_id}/lists       → Get board columns

### Cards
GET    /boards/{board_id}/cards     → List cards
POST   /cards                       → Create card
PUT    /cards/{id}                  → Update card
DELETE /cards/{id}                  → Delete card

### Worklogs (Time Tracking)
POST   /worklogs                          → Log hours
GET    /worklogs/card/{card_id}           → Hours per card
GET    /worklogs/me/week?week=YYYY-Www   → My weekly hours
PUT    /worklogs/{id}                     → Edit log (owner only)
DELETE /worklogs/{id}                     → Delete log (owner only)

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL running locally

### Backend
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

Create `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/neocare
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
cd backend
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000  
Swagger docs: http://127.0.0.1:8000/docs

### Frontend
```bash
cd frontend_t
npm install
npm run dev
```
App: http://localhost:5173

---

## 🧪 Testing

```bash
cd backend
pytest -v                        # Run all unit tests
pytest -k "not e2e"             # Skip E2E (requires Playwright)
pytest --cov=app tests/         # With coverage
```
44 passed, 1 warning

Tests use SQLite automatically — no PostgreSQL required for testing.

---

## 📁 Project Structure
NeoCare/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── auth/          # JWT auth
│       ├── boards/        # Kanban boards
│       ├── cards/         # Task cards
│       └── worklogs/      # Time tracking
├── frontend_t/
│   └── src/
│       ├── pages/
│       ├── components/
│       └── lib/
└── start-all.ps1          # Start everything (Windows)

---

## 📌 Status

- ✅ Backend API — complete and tested  
- ✅ JWT authentication  
- ✅ Time tracking system  
- ✅ Automated test suite (44 tests)  
- 🔜 Docker deployment  
- 🔜 CI/CD pipeline
