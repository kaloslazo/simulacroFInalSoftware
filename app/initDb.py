# app/init_db.py
from app.main import get_recommendations
from database import Base, engine, SessionLocal, Movie, UserPreference

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Precarga de datos
        movies = [
            Movie(title="The Dark Knight", genre="Action", rating=9.0, year=2008),
            Movie(title="Inception", genre="Sci-Fi", rating=8.8, year=2010),
            Movie(title="The Matrix", genre="Sci-Fi", rating=8.7, year=1999),
            Movie(title="Pulp Fiction", genre="Crime", rating=8.9, year=1994),
            Movie(title="Forrest Gump", genre="Drama", rating=8.8, year=1994)
        ]
        db.add_all(movies)

        preferences = [
            UserPreference(user_id=1, movie_min_rating=8.5, movie_genre="Action"),
            UserPreference(user_id=2, movie_min_rating=8.0, movie_genre="Sci-Fi"),
            UserPreference(user_id=3, movie_min_rating=8.7, movie_genre="Drama")
        ]
        db.add_all(preferences)

        db.commit()

        # Precalentar caché
        for user_id in [1, 2, 3]:
            get_recommendations(user_id, db)

    finally:
        db.close()