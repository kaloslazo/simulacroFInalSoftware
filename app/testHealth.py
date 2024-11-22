import requests
import time
import json

def test_health_endpoint():
    print("Probando endpoint health...")
    
    try:
        # Hacer múltiples llamadas para generar métricas
        for _ in range(5):
            response = requests.get("http://localhost:8000/health")
            print(f"\nIntento {_ + 1}:")
            print(f"Status Code: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
            time.sleep(1)  # Esperar 1 segundo entre llamadas
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health_endpoint()