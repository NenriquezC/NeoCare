"""
Script para validar la conectividad entre la app móvil y el backend.

Uso:
    python test_connectivity.py

Este script simula una petición de login desde la app móvil al backend
para verificar que la comunicación funciona correctamente.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime

# Configuración
BACKEND_URL = "http://192.168.1.39:8000/auth/login"
TEST_EMAIL = "movil@test.com"
TEST_PASSWORD = "123456"

url = BACKEND_URL
data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD
}

print("="*60)
print(f"Test de login - {datetime.now().strftime('%H:%M:%S')}")
print("="*60)
print(f"URL: {url}")
print(f"Email: {data['email']}")
print(f"Password: {data['password']}")
print()

try:
    print("Enviando petición POST...")
    response = requests.post(url, json=data, timeout=10)
    
    print(f"\n✓ Respuesta recibida")
    print(f"  Status Code: {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    
    if response.ok:
        print(f"\n✓✓ LOGIN EXITOSO ✓✓")
        data = response.json()
        print(f"  Token recibido: {data.get('access_token', 'N/A')[:60]}...")
        print(f"  Token Type: {data.get('token_type', 'N/A')}")
    else:
        print(f"\n✗ LOGIN FALLIDO")
        print(f"  Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("\n✗ ERROR: Timeout - El servidor no respondió en 10 segundos")
    print("  Posibles causas:")
    print("  - El backend no está corriendo")
    print("  - Firewall bloqueando la conexión")
    
except requests.exceptions.ConnectionError as e:
    print(f"\n✗ ERROR DE CONEXIÓN")
    print(f"  No se pudo conectar a {url}")
    print(f"  Posibles causas:")
    print(f"  - Backend no está corriendo en 192.168.1.39:8000")
    print(f"  - Firewall bloqueando el puerto 8000")
    print(f"  - IP incorrecta")
    print(f"\n  Detalles: {str(e)[:200]}")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}")
    print(f"  {str(e)[:200]}")

print("\n" + "="*60)
print("\nPara probar desde la app móvil, asegúrate de:")
print("  1. Estar en la misma red WiFi que la PC")
print("  2. Usar estas credenciales:")
print("     Email: movil@test.com")
print("     Password: 123456")
print("  3. La app debe apuntar a: http://192.168.1.39:8000")
print("="*60)
