import pytest

BASE_URL = "http://localhost:5173/"

def test_login_exitoso(page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[type=email]", "user@example.com")
    page.fill("input[type=password]", "string")
    page.click("button[type=submit]")
    page.wait_for_url("**/boards")
    ##assert "Bienvenido" in page.content() 

def test_login_fallido(page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[type=email]", "usuario@example.com")
    page.fill("input[type=password]", "incorrecta")
    page.click("button[type=submit]")
    page.wait_for_selector("text=No se ha podido iniciar sesión (API no disponible o credenciales incorrectas)")

def test_dashboard_protegido(page):
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/login")
    assert "/login" in page.url

def test_dashboard_con_token(page):
    page.goto(f"{BASE_URL}/login")
    page.evaluate("window.localStorage.setItem('token','TOKEN_JWT_DE_PRUEBA')")
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_url("**/dashboard")
    assert "/dashboard" in page.url
