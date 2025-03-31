from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

discover_filters = Blueprint('discover_filters', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@discover_filters.route('/genre/list', methods=['GET'])
def get_genre_list():
    try:
        # Get movie genres
        movie_response = requests.get(
            f"{BASE_URL}/genre/movie/list",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        # Get TV genres
        tv_response = requests.get(
            f"{BASE_URL}/genre/tv/list",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        
        movie_response.raise_for_status()
        tv_response.raise_for_status()
        
        return jsonify({
            'success': True,
            'movie_genres': movie_response.json()['genres'],
            'tv_genres': tv_response.json()['genres']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@discover_filters.route('/discover/<media_type>/<int:genre_id>', methods=['GET'])
def get_media_by_genre(media_type, genre_id):
    valid_media_types = ['movie', 'tv']
    if media_type not in valid_media_types:
        return jsonify({'success': False, 'error': 'Invalid media type. Use "movie" or "tv".'}), 400
    
    try:
        response = requests.get(
            f"{BASE_URL}/discover/{media_type}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "with_genres": genre_id,
                "sort_by": "popularity.desc",  # Most popular first
                "page": request.args.get('page', 1)  # Optional pagination
            }
        )
        response.raise_for_status()
        
        results = []
        for item in response.json()['results']:
            result = {
                'id': item['id'],
                'title': item['title'] if media_type == 'movie' else item['name'],
                'overview': item['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item['poster_path'] else None,
                'vote_average': item['vote_average'],
                'release_date': item.get('release_date', item.get('first_air_date', 'N/A')),
                'media_type': media_type
            }
            results.append(result)
        
        return jsonify({
            'success': True,
            'genre_id': genre_id,
            'page': response.json()['page'],
            'total_pages': response.json()['total_pages'],
            'results': results
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500