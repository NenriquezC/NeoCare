# Colección Postman - NeoCare API

## Descripción
Esta colección contiene todos los endpoints de la API de NeoCare con ejemplos listos para usar.

## Contenido
La colección incluye los siguientes grupos de endpoints:

### 1. **Auth** (Autenticación)
- **Register**: Registra un nuevo usuario
  - POST `/auth/register`
  - Body: `email`, `password`, `name`
  
- **Login**: Inicia sesión y obtiene token JWT
  - POST `/auth/login`
  - Body: `username` (email), `password`

### 2. **Boards** (Tableros)
- **Get All Boards**: Obtiene todos los tableros del usuario
  - GET `/boards/`
  - Requiere autenticación
  
- **Get Board Lists**: Obtiene las listas de un tablero
  - GET `/boards/{board_id}/lists/`
  - Requiere autenticación

### 3. **Cards** (Tarjetas)
- **Create Card**: Crea una nueva tarjeta
  - POST `/cards/`
  - Body: `title`, `description`, `due_date`, `board_id`, `list_id`
  
- **Get Cards by Board**: Obtiene todas las tarjetas de un tablero
  - GET `/cards/?board_id={board_id}`
  
- **Get Card by ID**: Obtiene una tarjeta específica
  - GET `/cards/{card_id}`
  
- **Update Card (PATCH)**: Actualiza parcialmente una tarjeta
  - PATCH `/cards/{card_id}`
  - Body: solo los campos a actualizar
  
- **Update Card (PUT)**: Actualiza completamente una tarjeta
  - PUT `/cards/{card_id}`
  
- **Delete Card**: Elimina una tarjeta
  - DELETE `/cards/{card_id}`

## Cómo importar en Postman

### Opción 1: Importar desde archivo
1. Abre Postman
2. Haz clic en **Import**
3. Selecciona **Upload Files**
4. Elige el archivo `NeoCare_Postman_Collection.json`
5. Haz clic en **Import**

### Opción 2: Copiar y pegar
1. Abre Postman
2. Haz clic en **Import**
3. Ve a la pestaña **Paste Raw Text**
4. Copia el contenido del JSON
5. Pégalo en el campo de texto
6. Haz clic en **Import**

## Variables de Postman

La colección incluye dos variables:
- `{{access_token}}`: Tu token JWT (obtenido al hacer login)
- `{{base_url}}`: URL base de la API (por defecto: `http://localhost:8000`)

### Cómo configurar las variables

1. Abre la colección en Postman
2. Haz clic en **Edit** (icono de lápiz)
3. Ve a la pestaña **Variables**
4. Actualiza los valores según sea necesario

## Flujo de uso recomendado

1. **Registrarse o Login**
   - Ejecuta `Auth > Register` o `Auth > Login`
   - Copia el `access_token` de la respuesta
   - Pégalo en la variable `{{access_token}}` en Postman

2. **Obtener tableros**
   - Ejecuta `Boards > Get All Boards`
   - Nota el ID del tablero que deseas usar

3. **Obtener listas del tablero**
   - Ejecuta `Boards > Get Board Lists` con el board_id
   - Nota los IDs de las listas

4. **Trabajar con tarjetas**
   - Ejecuta `Cards > Create Card` con board_id y list_id
   - Usa `Cards > Get Cards by Board` para listar tarjetas
   - Usa `Cards > Update Card` para modificar tarjetas
   - Usa `Cards > Delete Card` para eliminar tarjetas

## Ejemplos de payloads

### Registrar usuario
```json
{
  "email": "usuario@example.com",
  "password": "password123",
  "name": "Juan Pérez"
}
```

### Login
```
username: usuario@example.com
password: password123
```

### Crear tarjeta
```json
{
  "title": "Implementar login",
  "description": "Crear endpoint de login con JWT",
  "due_date": "2025-12-25",
  "board_id": 1,
  "list_id": 1
}
```

### Actualizar tarjeta (PATCH)
```json
{
  "title": "Nuevo título",
  "list_id": 2
}
```

## Notas importantes

- La API corre en `http://localhost:8000` (asegúrate de que esté ejecutándose)
- Todos los endpoints excepto **Register** y **Login** requieren autenticación
- El token JWT debe incluirse en el header: `Authorization: Bearer {token}`
- Los timestamps se devuelven en formato ISO 8601 con timezone UTC
- Las respuestas de error incluyen un mensaje descriptivo

## Código de estados HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Solicitud exitosa sin contenido |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o ausente |
| 403 | Forbidden - Sin permisos para este recurso |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Validación fallida |

## Solución de problemas

### "401 Unauthorized"
- Verifica que hayas incluido el token JWT en el header
- Asegúrate de que el token es válido y no haya expirado

### "403 Forbidden"
- El tablero o tarjeta no pertenece al usuario autenticado
- Verifica que estés usando los IDs correctos

### "404 Not Found"
- El recurso no existe
- Verifica que el ID sea correcto

### "422 Unprocessable Entity"
- Los datos enviados no cumplen la validación
- Revisa que todos los campos requeridos estén presentes y con el tipo correcto

## Contacto y soporte

Para más información sobre la API, consulta la documentación en:
- `/docs` - Swagger UI
- `/redoc` - ReDoc

O contacta al equipo de desarrollo de NeoCare.
