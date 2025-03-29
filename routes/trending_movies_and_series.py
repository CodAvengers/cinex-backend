from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

trending_routes = Blueprint('trending_routes', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@trending_routes.route('/trending/movies', methods=['GET'])
def get_trending_movies():
    try:
        # Get trending movies from TMDB (daily trend)
        response = requests.get(
            f"{BASE_URL}/trending/movie/day",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        response.raise_for_status()
        
        # Process the results
        trending_movies = []
        for movie in response.json()['results'][:20]:  # Get top 20 trending
            trending_movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                'vote_average': movie['vote_average'],
                'release_date': movie['release_date'],
                'popularity': movie['popularity'],
                'trending_rank': len(trending_movies) + 1  # Add ranking position
            })
        
        return jsonify({
            'success': True,
            'time_window': 'day',  # Can be changed to 'week'
            'results': trending_movies
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500