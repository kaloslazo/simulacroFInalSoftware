import pytest
import time
from .recommendation import MovieRecommender
from .database import Base, engine, Movie, UserPreference, get_db
from sqlalchemy.orm import Session

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    # Crear datos de prueba
    db = next(get_db())
    movie = Movie(title="Test Movie", genre="Action", rating=9.0, year=2024)
    db.add(movie)
    pref = UserPreference(user_id=1, movie_min_rating=8.0, movie_genre="Action")
    db.add(pref)
    db.commit()
    yield
    Base.metadata.drop_all(bind=engine)

def test_get_recommendations():
    db = next(get_db())
    recommender = MovieRecommender(db)
    recommendations = recommender.get_recommendations(user_id=1)
    assert len(recommendations) > 0
    assert all(r.rating >= 8.0 for r in recommendations)
    assert all(r.genre == "Action" for r in recommendations)

def test_similarity_score():
    db = next(get_db())
    recommender = MovieRecommender(db)
    movie = Movie(title="Score Test", genre="Action", rating=9.0, year=2024)
    pref = UserPreference(user_id=1, movie_min_rating=8.0, movie_genre="Action")
    
    score = recommender.calculate_similarity_score(movie, pref)
    assert 0 <= score <= 1
    assert score > 0.8  # Alta similitud para película que cumple preferencias

def test_cache_behavior():
    db = next(get_db())
    recommender = MovieRecommender(db)
    
    # Primera llamada
    start_time = time.time()
    recommendations1 = recommender.get_recommendations(user_id=1)
    time1 = time.time() - start_time
    
    # Segunda llamada (debería usar caché)
    start_time = time.time()
    recommendations2 = recommender.get_recommendations(user_id=1)
    time2 = time.time() - start_time
    
    assert recommendations1 == recommendations2
    assert time2 < time1  # La segunda llamada debería ser más rápida