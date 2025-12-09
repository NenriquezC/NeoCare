import pytest

BASE_URL = "http://localhost:3000"

def test_login_exitoso(page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name=email]", "usuario@example.com")
    page.fill("input[name=password]", "123456")
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard")
    assert "Bienvenido" in page.content()

def test_login_fallido(page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name=email]", "usuario@example.com")
    page.fill("input[name=password]", "incorrecta")
    page.click("button[type=submit]")
    page.wait_for_selector("text=Credenciales inválidas")

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
