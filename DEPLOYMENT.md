# 🚀 NeoCare Backend - Despliegue en Render

## Despliegue Backend

### 1. Preparar repositorio GitHub
```bash
cd backend
git init
git add .
git commit -m "Backend listo para producción"
git remote add origin https://github.com/TU_USUARIO/neocare-backend.git
git push -u origin main
```

### 2. Crear Base de Datos PostgreSQL

**Opción A: Railway**
1. Ve a https://railway.app
2. Crear nuevo proyecto → Add PostgreSQL
3. Copia el `DATABASE_URL`

**Opción B: Neon**
1. Ve a https://neon.tech
2. Crear proyecto → Copia connection string

### 3. Desplegar en Render

1. Ve a https://render.com
2. New+ → Web Service
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: neocare-backend
   - **Region**: Frankfurt (o el más cercano)
   - **Branch**: main
   - **Root Directory**: `backend` (si está en subdirectorio)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Se toma del Procfile automáticamente

5. **Variables de Entorno** (Environment):
   ```
   DATABASE_URL=postgresql://usuario:password@host:5432/neocare
   SECRET_KEY=tu-clave-super-secreta-cambiar-aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   TESTING=0
   ```

6. Click en **Create Web Service**

### 4. Ejecutar Migraciones

Una vez desplegado, ve a la Shell de Render:
```bash
alembic upgrade head
```

### 5. Verificar Despliegue

URL del backend: `https://neocare-backend.onrender.com`

Probar:
```bash
curl https://neocare-backend.onrender.com/
```

Debería responder:
```json
{"status": "NeoCare Backend Running"}
```

---

## Despliegue Frontend

### 1. Preparar Frontend

```bash
cd frontend_t
```

Crear `.env.production`:
```bash
VITE_API_URL=https://neocare-backend.onrender.com
```

### 2. Subir a GitHub

```bash
git init
git add .
git commit -m "Frontend listo para producción"
git remote add origin https://github.com/TU_USUARIO/neocare-frontend.git
git push -u origin main
```

### 3. Desplegar en Vercel

1. Ve a https://vercel.com
2. Import Project
3. Conecta tu repositorio de frontend
4. Configuración:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend_t` (si está en subdirectorio)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Environment Variables**:
   ```
   VITE_API_URL=https://neocare-backend.onrender.com
   ```

6. Click en **Deploy**

### 4. Verificar Despliegue

URL: `https://neocare-frontend.vercel.app`

---

## ⚠️ Notas Importantes

1. **Primera carga lenta**: Render en plan gratuito "hiberna" después de 15 min de inactividad. Primera petición puede tardar ~30s.

2. **CORS**: Ya configurado para Vercel en `app/main.py`

3. **Migraciones**: Ejecutar siempre que cambien los modelos:
   ```bash
   alembic revision --autogenerate -m "descripcion"
   alembic upgrade head
   ```

4. **Logs**: Ver en Render Dashboard → Logs

5. **Base de datos de prueba**: Poblar con datos de demo para la presentación

---

## 🔧 Troubleshooting

### Error: ModuleNotFoundError
- Verificar que `requirements.txt` tenga todas las dependencias
- Reconstruir servicio en Render

### Error: Database connection
- Verificar `DATABASE_URL` en variables de entorno
- Asegurar que BD PostgreSQL está activa

### Error: CORS
- Añadir dominio de Vercel a `allow_origins` en `app/main.py`
- Redesplegar

### Build falla
- Revisar logs en Render
- Verificar Python version (3.10+)
