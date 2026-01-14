"""
Script para ejecutar tests E2E de NeoCare
"""
import subprocess
import sys
import time
import requests

def verificar_backend():
    """Verifica si el backend está corriendo"""
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=2)
        print(f"✅ Backend corriendo - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Backend NO está corriendo: {e}")
        return False

def ejecutar_tests():
    """Ejecuta los tests E2E"""
    print("\n🧪 Ejecutando tests E2E de API...\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/e2e/", "-v", "-k", "test_api", "--tb=short"],
        cwd="C:\\Desarrollo\\github\\NeoCare\\backend"
    )

    return result.returncode

if __name__ == "__main__":
    print("=" * 60)
    print("Tests E2E de NeoCare - API")
    print("=" * 60)

    # Verificar backend
    if not verificar_backend():
        print("\n⚠️  Por favor, inicia el backend primero:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload\n")
        sys.exit(1)

    # Ejecutar tests
    exit_code = ejecutar_tests()

    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ TODOS LOS TESTS PASARON")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
    print("=" * 60)

    sys.exit(exit_code)

