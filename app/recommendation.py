from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import time
from functools import lru_cache
from .database import Movie, UserPreference

class MovieRecommender:
    def __init__(self, db: Session):
        self.db = db

    @lru_cache(maxsize=1000)
    def get_recommendations(self, user_id: int, limit: int = 5) -> List[Movie]:
        start_time = time.time()
        
        # Usar caché para preferencias
        user_prefs = self.db.query(UserPreference)\
            .filter(UserPreference.user_id == user_id)\
            .first()
            
        if not user_prefs:
            return []

        # Query optimizada
        recommendations = self.db.query(Movie)\
            .filter(
                Movie.genre == user_prefs.movie_genre,
                Movie.rating >= user_prefs.movie_min_rating
            )\
            .order_by(
                desc(Movie.rating),
                desc(Movie.year)
            )\
            .limit(limit)\
            .all()

        return recommendations

    def calculate_similarity_score(self, movie: Movie, user_prefs: UserPreference) -> float:
        GENRE_WEIGHT = 0.6
        RATING_WEIGHT = 0.4
        
        genre_score = 1.0 if movie.genre == user_prefs.movie_genre else 0.0
        rating_score = min(1.0, movie.rating / 10.0)
        
        return (genre_score * GENRE_WEIGHT) + (rating_score * RATING_WEIGHT)