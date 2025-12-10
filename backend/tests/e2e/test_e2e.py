import pytest

BASE_URL = "http://localhost:5173/"

"""
Pruebas E2E de autenticación y protección de rutas usando Playwright + pytest.

Este módulo contiene pruebas que verifican:
- Inicio de sesión exitoso y redirección al listado de tableros (/boards).
- Manejo de inicio de sesión fallido con mensaje de error visible.
- Protección de la ruta /dashboard para usuarios no autenticados.
- Acceso a /dashboard cuando existe un token simulado en localStorage.

Notas:
- Estas pruebas asumen que la aplicación frontend está disponible en BASE_URL.
- Los selectores utilizados (input[type=email], input[type=password], button[type=submit]) se basan en la estructura actual del formulario de login.
- La comprobación que valida contenido textual de la página en test_login_exitoso está comentada; descomentar si se desea verificar texto visible.
"""

def test_login_exitoso(page):
    """Verifica que un usuario con credenciales válidas pueda iniciar sesión.

    Flujo de la prueba:
    1. Navega a la página de login.
    2. Rellena los campos de email y contraseña con credenciales válidas.
    3. Envía el formulario de login.
    4. Espera a que la aplicación redirija a la ruta de tableros (/boards).

    Aserciones/condiciones:
    - Se espera una redirección a una URL que contenga '/boards'.
    - Hay una comprobación comentada que valida la presencia del texto "Bienvenido" en el contenido de la página;
    descomentar si se desea validar también el contenido textual.
    """
    page.goto(f"{BASE_URL}/login")
    page.fill("input[type=email]", "user@example.com")
    page.fill("input[type=password]", "string")
    page.click("button[type=submit]")
    page.wait_for_url("**/boards")
    ##assert "Bienvenido" in page.content() 

def test_login_fallido(page):
    """Verifica que el sistema muestra un mensaje de error cuando las credenciales son incorrectas.

    Flujo de la prueba:
    1. Navega a la página de login.
    2. Rellena los campos de email y contraseña con credenciales incorrectas.
    3. Envía el formulario de login.
    4. Espera a que aparezca un selector con el mensaje de error esperado.

    Aserciones/condiciones:
    - Se espera que el selector de texto con el mensaje de error esté presente:
    "No se ha podido iniciar sesión (API no disponible o credenciales incorrectas)".
    """
    page.goto(f"{BASE_URL}/login")
    page.fill("input[type=email]", "usuario@example.com")
    page.fill("input[type=password]", "incorrecta")
    page.click("button[type=submit]")
    page.wait_for_selector("text=No se ha podido iniciar sesión (API no disponible o credenciales incorrectas)")

def test_dashboard_protegido(page):
    """Verifica que la ruta /dashboard está protegida y redirige a /login si no hay token.

    Flujo de la prueba:
    1. Intenta navegar directamente a /dashboard sin establecer token en localStorage.
    2. Espera la redirección a la página de login.

    Aserciones/condiciones:
    - La URL final contiene '/login', lo que indica que el acceso fue denegado y se pidió autenticación.
    """

    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/login")
    assert "/login" in page.url

def test_dashboard_con_token(page):
    """Verifica que al establecer un token en localStorage se puede acceder a /dashboard.

    Flujo de la prueba:
    1. Navega a la página de login (para obtener el mismo origen y poder manipular localStorage).
    2. Inserta un token simulado en window.localStorage.
    3. Navega a /dashboard.
    4. Espera la redirección/permiso de acceso a la ruta de dashboard.

    Aserciones/condiciones:
    - La URL final contiene '/dashboard', indicando acceso correcto con token presente.
    - El token usado es un placeholder; si la aplicación valida el token en el backend, puede ser necesario mockear la respuesta de la API.
    """
    page.goto(f"{BASE_URL}/login")
    page.evaluate("window.localStorage.setItem('token','TOKEN_JWT_DE_PRUEBA')")
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/dashboard")
    assert "/dashboard" in page.url
