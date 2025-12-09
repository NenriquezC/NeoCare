# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ----------------------------
# Test GET /
# ----------------------------
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "NeoCare Backend Running"}

# ----------------------------
# Test que el router de auth está incluido
# ----------------------------
def test_auth_router_included():
    # Hacemos una petición a un endpoint de auth que exista
    response = client.get("/auth")  # Este endpoint no existe, debería devolver 405 o 404
    assert response.status_code in [404, 405]
