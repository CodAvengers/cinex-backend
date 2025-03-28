from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

tmdb_routes = Blueprint('tmdb_routes', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@tmdb_routes.route('/top-rated/movies', methods=['GET'])
def get_top_rated_movies():
    try:
        response = requests.get(
            f"{BASE_URL}/movie/top_rated",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        )
        response.raise_for_status()
        
        movies = []
        for movie in response.json()['results'][:10]:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                'vote_average': movie['vote_average'],
                'release_date': movie['release_date'],
                'media_type': 'movie'
            })
        
        return jsonify({'success': True, 'results': movies})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tmdb_routes.route('/top-rated/tv', methods=['GET'])
def get_top_rated_tv():
    try:
        response = requests.get(
            f"{BASE_URL}/tv/top_rated",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        )
        response.raise_for_status()
        
        tv_shows = []
        for show in response.json()['results'][:10]:
            tv_shows.append({
                'id': show['id'],
                'title': show['name'],
                'overview': show['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{show['poster_path']}" if show['poster_path'] else None,
                'vote_average': show['vote_average'],
                'first_air_date': show['first_air_date'],
                'media_type': 'tv'
            })
        
        return jsonify({'success': True, 'results': tv_shows})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tmdb_routes.route('/top-rated/all', methods=['GET'])
def get_top_rated_all():
    try:
        movies_response = requests.get(
            f"{BASE_URL}/movie/top_rated",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        )
        tv_response = requests.get(
            f"{BASE_URL}/tv/top_rated",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        )
        movies_response.raise_for_status()
        tv_response.raise_for_status()
        
        combined = []
        
        for movie in movies_response.json()['results'][:10]:
            combined.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                'vote_average': movie['vote_average'],
                'date': movie['release_date'],
                'media_type': 'movie'
            })
        
        for show in tv_response.json()['results'][:10]:
            combined.append({
                'id': show['id'],
                'title': show['name'],
                'overview': show['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{show['poster_path']}" if show['poster_path'] else None,
                'vote_average': show['vote_average'],
                'date': show['first_air_date'],
                'media_type': 'tv'
            })
        
        combined.sort(key=lambda x: x['vote_average'], reverse=True)
        
        return jsonify({'success': True, 'results': combined[:20]})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500