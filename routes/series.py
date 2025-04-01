from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

series_bp = Blueprint('series', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# List latest series from TMDb
@series_bp.route('/api/series/latest', methods=['GET'])
def list_series():
    try:
        url = f"https://api.themoviedb.org/3/tv/airing_today?api_key={TMDB_API_KEY}&language=en-US&page=1"
        print(f"Fetching series: {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Series response: {data}")
        series = data['results']

        for show in series:
            tmdb_id = show.get('id')
            if tmdb_id:
                external_ids_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
                print(f"Requesting external IDs for series {tmdb_id}: {external_ids_url}")
                external_response = requests.get(external_ids_url)
                external_response.raise_for_status()
                external_data = external_response.json()
                show['imdb_id'] = external_data.get('imdb_id', None)
                print(f"Added IMDb ID for series {tmdb_id}: {show['imdb_id']}")

        return jsonify(series)
    except Exception as e:
        print(f"Series error: {str(e)}")
        return jsonify({"error": str(e)}), 500