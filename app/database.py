from sqlalchemy import create_engine, Column, Integer, String, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String, index=True)
    rating = Column(Float, index=True)
    year = Column(Integer)

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    movie_min_rating = Column(Float)
    movie_genre = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Limpiar datos existente
        db.query(Movie).delete()
        db.query(UserPreference).delete()
        
        movies = [
            Movie(title="The Dark Knight", genre="Action", rating=9.0, year=2008),
            Movie(title="Inception", genre="Sci-Fi", rating=8.8, year=2010),
            Movie(title="The Matrix", genre="Sci-Fi", rating=8.7, year=1999),
            Movie(title="Pulp Fiction", genre="Crime", rating=8.9, year=1994),
            Movie(title="Forrest Gump", genre="Drama", rating=8.8, year=1994)
        ]
        db.bulk_save_objects(movies)
        
        preferences = [
            UserPreference(user_id=1, movie_min_rating=8.5, movie_genre="Action"),
            UserPreference(user_id=2, movie_min_rating=8.0, movie_genre="Sci-Fi"),
            UserPreference(user_id=3, movie_min_rating=8.7, movie_genre="Drama"),
            UserPreference(user_id=4, movie_min_rating=8.5, movie_genre="Fantasy")
        ]
        db.bulk_save_objects(preferences)
        
        db.commit()
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()