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

# Blueprint for search routes
search_routes = Blueprint("search_routes", __name__)

# Helper function to fetch search results
def fetch_tmdb_search(endpoint, query):
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    url = f"{BASE_URL}/search/{endpoint}?api_key={TMDB_API_KEY}&query={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError if the status is not 200
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

# Search for movies, TV shows, or people in one query
@search_routes.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    return fetch_tmdb_search("multi", query)

# Search for movies only
@search_routes.route("/search/movie", methods=["GET"])
def search_movie():
    query = request.args.get("query")
    return fetch_tmdb_search("movie", query)

# Search for TV shows only
@search_routes.route("/search/tv", methods=["GET"])
def search_tv_show():
    query = request.args.get("query")
    return fetch_tmdb_search("tv", query)
