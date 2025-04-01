from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

movie_details_bp = Blueprint('movie_details', __name__, url_prefix='/api')

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
VIDSRC_BASE = os.getenv("VIDSRC_BASE")
VIDLINK_BASE = os.getenv("VIDLINK_BASE")

# Get detailed movie or series information
@movie_details_bp.route('/movie/details/<tmdb_id>', methods=['GET'])
def get_movie_details(tmdb_id):
    try:
        movie_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=credits"
        movie_response = requests.get(movie_details_url)
        
        is_movie = movie_response.status_code == 200
        media_type = 'movie' if is_movie else 'tv'

        details_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=credits"
        print(f"Fetching {media_type} details: {details_url}")
        response = requests.get(details_url)
        response.raise_for_status()
        data = response.json()
        print(f"{media_type.capitalize()} details response: {data}")

        genre_list_url = f"https://api.themoviedb.org/3/genre/{media_type}/list?api_key={TMDB_API_KEY}&language=en-US"
        genre_response = requests.get(genre_list_url)
        genre_response.raise_for_status()
        genre_data = genre_response.json()
        genre_map = {genre['id']: genre['name'] for genre in genre_data['genres']}

        title = data.get('title', data.get('name', 'Unknown Title'))
        overview = data.get('overview', 'No description available.')
        rating = data.get('vote_average', 0)
        release_date = data.get('release_date', data.get('first_air_date', ''))
        poster_path = data.get('poster_path', None)
        genres = [genre_map.get(genre_id, 'Unknown') for genre_id in data.get('genre_ids', [])]
        cast = [
            {
                'name': member['name'],
                'profile_path': member.get('profile_path', None),
                'character': member.get('character', 'Unknown')
            }
            for member in data.get('credits', {}).get('cast', [])[:5]
        ]

        quality = "Unknown"
        if release_date:
            year = int(release_date.split('-')[0])
            if year < 2000:
                quality = "Camera Copy"
            elif year >= 2010:
                quality = "HD"
            else:
                quality = "SD"

        details = {
            "title": title,
            "overview": overview,
            "rating": rating,
            "release_date": release_date,
            "poster_path": poster_path,
            "genres": genres,
            "cast": cast,
            "quality": quality,
            "tmdb_id": tmdb_id,
            "media_type": media_type
        }
        return jsonify(details)
    except requests.RequestException as e:
        print(f"Request Error: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Get embed URLs for both VidSrc and VidLink
@movie_details_bp.route('/movie/embed/<tmdb_id>', methods=['GET'])
def get_movie_embed(tmdb_id):
    try:
        movie_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
        movie_response = requests.get(movie_details_url)
        
        is_movie = movie_response.status_code == 200
        media_type = 'movie' if is_movie else 'tv'

        external_ids_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
        print(f"Requesting external IDs: {external_ids_url}")
        external_response = requests.get(external_ids_url)
        external_response.raise_for_status()
        external_data = external_response.json()
        print(f"External IDs response: {external_data}")

        imdb_id = external_data.get('imdb_id', None)
        if not imdb_id:
            return jsonify({"error": "No IMDb ID found for VidSrc"}), 404

        if is_movie:
            vidsrc_url = f"{VIDSRC_BASE}/embed/movie?imdb={imdb_id}"
            vidlink_url = f"{VIDLINK_BASE}/movie/{tmdb_id}?primaryColor=63b8bc&secondaryColor=a2a2a2&iconColor=eefdec&icons=default&title=true&poster=true&autoplay=false"
        else:
            vidsrc_url = f"{VIDSRC_BASE}/embed/tv?imdb={imdb_id}&season=1&episode=1"
            vidlink_url = f"{VIDLINK_BASE}/tv/{tmdb_id}/1/1?primaryColor=63b8bc&secondaryColor=a2a2a2&iconColor=eefdec&icons=default&title=true&poster=true&autoplay=false"

        print(f"Generated VidSrc URL: {vidsrc_url}")
        print(f"Generated VidLink URL: {vidlink_url}")

        return jsonify({
            "vidsrc_url": vidsrc_url,
            "vidlink_url": vidlink_url,
            "media_type": media_type
        })
    except requests.RequestException as e:
        print(f"Request Error: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500