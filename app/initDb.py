from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal, Movie, UserPreference

def init_movies(db: Session):
    # Limpiar datos existentes
    db.query(Movie).delete()
    
    movies = [
        Movie(title="The Dark Knight", genre="Action", rating=9.0, year=2008),
        Movie(title="Inception", genre="Sci-Fi", rating=8.8, year=2010),
        Movie(title="The Matrix", genre="Sci-Fi", rating=8.7, year=1999),
        Movie(title="Pulp Fiction", genre="Crime", rating=8.9, year=1994),
        Movie(title="Forrest Gump", genre="Drama", rating=8.8, year=1994)
    ]
    db.bulk_save_objects(movies)
    db.commit()
    return movies

def init_preferences(db: Session):
    # Limpiar datos existentes
    db.query(UserPreference).delete()
    
    preferences = [
        UserPreference(user_id=1, movie_min_rating=8.5, movie_genre="Action"),
        UserPreference(user_id=2, movie_min_rating=8.0, movie_genre="Sci-Fi"),
        UserPreference(user_id=3, movie_min_rating=8.7, movie_genre="Drama")
    ]
    db.bulk_save_objects(preferences)
    db.commit()
    return preferences

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_movies(db)
        init_preferences(db)
        return True
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        db.rollback()
        return False
    finally:
        db.close()