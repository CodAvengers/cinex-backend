from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Define blueprint for popular routes
popular_routes = Blueprint('popular_routes', __name__)

# Route for popular movies
@popular_routes.route('/movies/popular')
def popular_movies():
    url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'No popular movies found'}), 400
    return jsonify(response.json())

# Route for popular series
@popular_routes.route('/series/popular')
def popular_series():
    url = f"{BASE_URL}/tv/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'No popular tv shows found'}), 400
    return jsonify(response.json())
