from fastapi.testclient import TestClient
from .main import app
from .database import init_database, Base, engine, get_db
from sqlalchemy.orm import Session
import pytest

# Crear un cliente de prueba
client = TestClient(app)

# Fixture para la base de datos de prueba
@pytest.fixture(autouse=True)
def setup_database():
    # Crear todas las tablas antes de cada test
    Base.metadata.create_all(bind=engine)
    # Inicializar datos de prueba
    init_database()
    yield
    # Limpiar después de cada test
    Base.metadata.drop_all(bind=engine)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_get_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Verificar que hay películas

def test_create_preference():
    preference = {
        "user_id": 1,
        "movie_min_rating": 8.5,
        "movie_genre": "Action"
    }
    response = client.post("/preferences/", json=preference)
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

def test_get_recommendations():
    # Primero crear una preferencia
    preference = {
        "user_id": 1,
        "movie_min_rating": 8.5,
        "movie_genre": "Action"
    }
    client.post("/preferences/", json=preference)
    
    # Luego obtener recomendaciones
    response = client.get("/recommendations/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)