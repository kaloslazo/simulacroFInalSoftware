import pytest
from sqlalchemy.orm import Session
from .database import Base, engine, get_db, Movie, UserPreference
from .initDb import init_movies, init_preferences, init_db

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_init_movies(db_session):
    # Probar la inicialización de películas
    movies = init_movies(db_session)
    assert len(movies) == 5
    
    # Verificar una película específica
    dark_knight = db_session.query(Movie).filter(Movie.title == "The Dark Knight").first()
    assert dark_knight is not None
    assert dark_knight.rating == 9.0
    assert dark_knight.genre == "Action"

def test_init_preferences(db_session):
    # Probar la inicialización de preferencias
    preferences = init_preferences(db_session)
    assert len(preferences) == 3
    
    # Verificar una preferencia específica
    action_pref = db_session.query(UserPreference).filter(
        UserPreference.movie_genre == "Action"
    ).first()
    assert action_pref is not None
    assert action_pref.movie_min_rating == 8.5

def test_init_db():
    # Probar la inicialización completa
    result = init_db()
    assert result is True
    
    # Verificar que los datos se crearon correctamente
    db = next(get_db())
    try:
        movies_count = db.query(Movie).count()
        preferences_count = db.query(UserPreference).count()
        assert movies_count == 5
        assert preferences_count == 3
    finally:
        db.close()

def test_init_db_idempotent(db_session):
    # Verificar que ejecutar init_db múltiples veces es seguro
    first_result = init_db()
    second_result = init_db()
    assert first_result is True
    assert second_result is True
    
    # Verificar que no se duplicaron los datos
    movies_count = db_session.query(Movie).count()
    preferences_count = db_session.query(UserPreference).count()
    assert movies_count == 5
    assert preferences_count == 3