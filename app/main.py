from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import time
from .database import get_db, Movie, UserPreference, init_database

app = FastAPI()

# Cache en memoria
recommendations_cache = {}

@app.on_event("startup")
async def startup_event():
    init_database()

@app.get("/")
async def root():
    return {
        "message": "Examen final de Ingenieria de Software - 2024.2",
        "team": ["Kalos Lazo", "Lenin Chavez"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "metrics": {
            "availability": 100.0,
            "reliability": 100.0
        }
    }

@app.get("/movies/")
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Movie).offset(skip).limit(limit).all()

@app.post("/preferences/")
def create_preference(preference: dict, db: Session = Depends(get_db)):
    try:
        db_preference = UserPreference(**preference)
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
        return db_preference
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    try:
        # Verificar caché
        cache_key = f"user_{user_id}"
        if cache_key in recommendations_cache:
            return recommendations_cache[cache_key]

        # Obtener preferencias
        user_pref = db.query(UserPreference)\
            .filter(UserPreference.user_id == user_id)\
            .first()
            
        if not user_pref:
            return []

        # Buscar películas
        movies = db.query(Movie)\
            .filter(
                Movie.genre == user_pref.movie_genre,
                Movie.rating >= user_pref.movie_min_rating
            )\
            .order_by(Movie.rating.desc())\
            .limit(5)\
            .all()
            
        # Guardar en caché
        recommendations_cache[cache_key] = movies
        return movies

    except Exception as e:
        print(f"Error en recomendaciones: {e}")
        return []
