"""
test_auth.py
------------

Conjunto de pruebas end-to-end para el flujo de autenticación y la protección
de la ruta /dashboard de una aplicación web, usando Playwright en combinación
con pytest.

Cada prueba está documentada con un docstring que describe su propósito, los
pasos realizados y las aserciones esperadas. Estas pruebas asumen que existe
un fixture `page` proporcionado por Playwright (pytest-playwright).
"""

import pytest

# URL base de la aplicación bajo prueba. Mantenerlo aquí facilita cambiar el
# entorno (local, staging, CI) sin modificar las pruebas individuales.
BASE_URL = "http://localhost:3000"

def test_login_exitoso(page):
    """
    Prueba de inicio de sesión exitoso.

    Pasos:
    1. Navegar a la página de login.
    2. Rellenar los campos de email y contraseña con credenciales válidas.
    3. Enviar el formulario de autenticación.
    4. Esperar la redirección al dashboard.

    Aserciones:
    - La URL resultante corresponde al dashboard.
    - El contenido de la página contiene el texto "Bienvenido", indicando que
    el usuario fue autenticado correctamente y que la interfaz muestra un
    saludo de bienvenida.
    """
    # Abrir la página de login
    page.goto(f"{BASE_URL}/login")

    # Rellenar credenciales válidas
    page.fill("input[name=email]", "usuario@example.com")
    page.fill("input[name=password]", "123456")

    # Enviar formulario
    page.click("button[type=submit]")

    # Esperar la redirección al dashboard (comodín para aceptar subrutas)
    page.wait_for_url("**/dashboard")

    # Comprobar que la página muestra un saludo de bienvenida
    assert "Bienvenido" in page.content()

def test_login_fallido(page):
    """
    Prueba de manejo de credenciales inválidas en el inicio de sesión.

    Pasos:
    1. Navegar a la página de login.
    2. Rellenar el email con un usuario válido pero la contraseña con un valor
        incorrecto.
    3. Enviar el formulario.
    4. Esperar que se muestre el mensaje de error específico "Credenciales inválidas".

    Aserciones:
    - Se detecta y muestra el mensaje de error esperado en la interfaz.
    """
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name=email]", "usuario@example.com")
    page.fill("input[name=password]", "incorrecta")
    page.click("button[type=submit]")

    # Esperar que aparezca un selector con el texto de error esperado.
    page.wait_for_selector("text=Credenciales inválidas")

def test_dashboard_protegido(page):
    """
    Verifica que la ruta /dashboard esté protegida para usuarios no autenticados.

    Pasos:
    1. Intentar acceder directamente a /dashboard sin haber iniciado sesión.
    2. Esperar la redirección a la página de login.

    Aserciones:
    - La URL actual contiene '/login', confirmando que el acceso fue denegado y
    el usuario fue redirigido para autenticarse.
    """

    # Acceso directo al dashboard sin token ni sesión previa
    page.goto(f"{BASE_URL}/dashboard")

    # La aplicación debe redirigir a /login si la ruta requiere autenticación
    page.wait_for_url("**/login")
    assert "/login" in page.url

def test_dashboard_con_token(page):
    """
    Comprueba que un usuario con token válido en localStorage puede acceder al dashboard.

    Pasos:
    1. Navegar a /login (para inicializar el contexto del navegador).
    2. Inyectar un token JWT simulado en localStorage.
    3. Navegar a /dashboard.
    4. Esperar la carga del dashboard.

    Aserciones:
    - La URL resultante corresponde a /dashboard, indicando que la aplicación
    reconoció el token y permitió el acceso.
    Notas:
    - En entornos de integración/CI puede ser preferible usar mecanismos de
    autenticación más realistas (ej. endpoints de login o fixtures de sesión).
    """
    page.goto(f"{BASE_URL}/login")

    # Simular la existencia de un token JWT en localStorage para evitar el flujo
    # completo de autenticación en estas pruebas unitarias de integración.
    page.evaluate("window.localStorage.setItem('token','TOKEN_JWT_DE_PRUEBA')")

    # Intentar acceder al dashboard con el token presente
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/dashboard")
    assert "/dashboard" in page.url