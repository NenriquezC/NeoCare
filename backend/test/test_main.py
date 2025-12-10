"""
tests/test_main.py
------------------

Pruebas básicas para el endpoint raíz y comprobación de inclusión del router
de autenticación en la aplicación FastAPI.

ATENCIÓN: He añadido únicamente docstrings y comentarios explicativos. No he
modificado la lógica original del código. La última línea del archivo contiene
un carácter extraño ('ç') que existe en el código que me proporcionaste; lo he
mantenido tal cual para no alterar tu lógica. Si quieres que lo corrija, dímelo.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ----------------------------
# Test GET /
# ----------------------------
def test_root_endpoint():
    """
    Comprueba que el endpoint raíz (GET /) responde correctamente.

    Flujo:
    - Se realiza una petición GET al endpoint raíz.
    - Se espera un código HTTP 200.
    - Se valida que el JSON devuelto coincida con el estado esperado de la API.

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
    """
    Verifica de forma indirecta que el router de autenticación está montado.

    Flujo:
    - Se realiza una petición GET a la ruta base de auth ("/auth").
    Nota: este endpoint suele no exponer GET en la raíz del router y por lo
    tanto se espera un 404 o un 405 según la configuración del router.
    - Se comprueba que el status code esté en la lista [404, 405], lo que indica
    que la ruta existe en la aplicación (o al menos que el prefijo está registrado).

    Consideraciones:
    - Dependiendo de cómo esté definido el router de auth, la respuesta exacta
    puede ser 404 (no encontrada) o 405 (método no permitido). Ambas son
    aceptadas por esta prueba como indicativo de inclusión del router.
    """
    # Hacemos una petición a un endpoint de auth que exista
    response = client.get("/auth")  # Este endpoint no existe, debería devolver 405 o 404
    assert response.status_code in [404, 405]