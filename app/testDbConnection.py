import pytest
from sqlalchemy.orm import Session
from .database import get_db, Movie, UserPreference, init_database, Base, engine

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    init_database()
    yield
    Base.metadata.drop_all(bind=engine)

def test_db_connection():
    db = next(get_db())
    assert isinstance(db, Session)
    db.close()

def test_movie_creation():
    db = next(get_db())
    movie = Movie(
        title="Test Movie",
        genre="Action",
        rating=8.5,
        year=2024
    )
    db.add(movie)
    db.commit()
    
    fetched_movie = db.query(Movie).filter(Movie.title == "Test Movie").first()
    assert fetched_movie is not None
    assert fetched_movie.genre == "Action"
    db.close()

def test_user_preference_creation():
    db = next(get_db())
    pref = UserPreference(
        user_id=999,
        movie_min_rating=7.5,
        movie_genre="Sci-Fi"
    )
    db.add(pref)
    db.commit()
    
    fetched_pref = db.query(UserPreference).filter(UserPreference.user_id == 999).first()
    assert fetched_pref is not None
    assert fetched_pref.movie_genre == "Sci-Fi"
    db.close()