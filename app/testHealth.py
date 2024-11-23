from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_health_metrics():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "availability" in data["metrics"]
    assert "reliability" in data["metrics"]
    assert data["metrics"]["availability"] == 100.0
    assert data["metrics"]["reliability"] == 100.0

def test_consecutive_health_checks():
    # Realizar múltiples llamadas para verificar consistencia
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"