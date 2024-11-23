from fastapi.testclient import TestClient
from .main import app
from .database import Base, engine
import pytest
import time

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_recommendation_cache():
    # Crear preferencia
    preference = {
        "user_id": 1,
        "movie_min_rating": 8.5,
        "movie_genre": "Action"
    }
    client.post("/preferences/", json=preference)
    
    # Primera llamada - sin caché
    start_time = time.time()
    response1 = client.get("/recommendations/1")
    time1 = time.time() - start_time
    
    # Segunda llamada - con caché
    start_time = time.time()
    response2 = client.get("/recommendations/1")
    time2 = time.time() - start_time
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert time2 < time1  # La segunda llamada debería ser más rápida

def test_error_handling():
    # Probar preferencia inválida
    invalid_preference = {
        "user_id": "invalid",
        "movie_min_rating": "invalid",
        "movie_genre": 123
    }
    response = client.post("/preferences/", json=invalid_preference)
    assert response.status_code == 500

def test_pagination():
    response = client.get("/movies/?skip=0&limit=2")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) <= 2

def test_performance():
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 0.001  # Verificar que responde en menos de 1ms