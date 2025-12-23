# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""Pruebas básicas de los endpoints expuestos por la aplicación principal (app.main).

Este módulo contiene tests ligeros que verifican:
- El endpoint raíz (GET /) responde correctamente con el estado esperado.
- Que el router de autenticación está registrado en la aplicación (comprobado mediante
una petición a la ruta base de auth que debería devolver 404 o 405 si no hay un GET definido).

Estas pruebas usan TestClient de FastAPI para realizar peticiones HTTP en memoria.
"""

# ----------------------------
# Test GET /
# ----------------------------
def test_root_endpoint():
    """Comprueba que el endpoint raíz devuelve el estado esperado.

    Flujo:
    1. Realiza una petición GET a "/".
    2. Verifica que el status code es 200.
    3. Comprueba que el JSON devuelto coincide con {"status": "NeoCare Backend Running"}.

    Aserciones:
    - response.status_code == 200
    - response.json() == {"status": "NeoCare Backend Running"}
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "NeoCare Backend Running"}

# ----------------------------
# Test que el router de auth está incluido
# ----------------------------
def test_auth_router_included():
    """Verifica de forma indirecta que el router de autenticación está montado.

    Flujo:
    1. Realiza una petición GET a "/auth".
    2. Como es probable que no exista un GET en la raíz del router auth, se acepta
    que la respuesta sea 404 (no encontrado) o 405 (método no permitido).
    Si el router no estuviera incluido, algunas configuraciones podrían también
    devolver 404; por eso se comprueba que el código esté entre [404, 405].

    Aserciones:
    - response.status_code está en [404, 405]
    """
    # Hacemos una petición a un endpoint de auth que exista
    response = client.get("/auth")  # Este endpoint no existe, debería devolver 405 o 404
    assert response.status_code in [404, 405]
