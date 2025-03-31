from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Ensure API key is loaded
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is not set in the environment variables!")

# Blueprint for top-rated routes
top_rated_routes = Blueprint("top_rated_routes", __name__)

# Helper function to fetch data
def fetch_tmdb_data(endpoint):
    url = f"{BASE_URL}/{endpoint}?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError if the status is not 200
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

# Route for top-rated movies
@top_rated_routes.route("/top_rated/movies", methods=["GET"])
def top_rated_movies():
    return fetch_tmdb_data("movie/top_rated")

# Route for top-rated TV shows
@top_rated_routes.route("/top_rated/tv", methods=["GET"])
def top_rated_tv():
    return fetch_tmdb_data("tv/top_rated")
