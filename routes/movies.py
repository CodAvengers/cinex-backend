from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

movies_bp = Blueprint('movies', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# List latest movies from TMDb
@movies_bp.route('/api/movies/latest', methods=['GET'])
def list_movies():
    try:
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
        print(f"Fetching movies: {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Movies response: {data}")
        movies = data['results']

        for movie in movies:
            tmdb_id = movie.get('id')
            if tmdb_id:
                external_ids_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
                print(f"Requesting external IDs for movie {tmdb_id}: {external_ids_url}")
                external_response = requests.get(external_ids_url)
                external_response.raise_for_status()
                external_data = external_response.json()
                movie['imdb_id'] = external_data.get('imdb_id', None)
                print(f"Added IMDb ID for movie {tmdb_id}: {movie['imdb_id']}")

                details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
                details_response = requests.get(details_url)
                details_response.raise_for_status()
                details_data = details_response.json()
                release_date = details_data.get('release_date', '')
                movie['release_date'] = release_date

                quality = "Unknown"
                if release_date:
                    year = int(release_date.split('-')[0])
                    if year < 2000:
                        quality = "Camera Copy"
                    elif year >= 2010:
                        quality = "HD"
                    else:
                        quality = "SD"
                movie['quality'] = quality

        return jsonify(movies)
    except Exception as e:
        print(f"Movies error: {str(e)}")
        return jsonify({"error": str(e)}), 500