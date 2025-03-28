from flask import Blueprint, request, jsonify 
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY') 
BASE_URL = "https://api.themoviedb.org/3"

#blueprint for top rated routes
top_rated_routes = Blueprint('top_rated_routes', __name__)

#route for top rated movies
@top_rated_routes.route('/top_rated/movies', methods=['GET'])
def top_rated_movies():
    url = f"{BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "No movies found"}), 404
    results = response.json()
    return jsonify(results)