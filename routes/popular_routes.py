from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Ensure API key is loaded
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is not set in the environment variables!")

# Define blueprint for popular routes
popular_routes = Blueprint("popular_routes", __name__)

# Helper function to fetch popular content
def fetch_popular(endpoint, content_type):
    url = f"{BASE_URL}/{endpoint}/popular?api_key={TMDB_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError if status is not 200
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"No popular {content_type} found", "details": str(e)}), 500

# Route for popular movies
@popular_routes.route("/movies/popular", methods=["GET"])
def popular_movies():
    return fetch_popular("movie", "movies")

# Route for popular TV series
@popular_routes.route("/series/popular", methods=["GET"])
def popular_series():
    return fetch_popular("tv", "TV shows")
