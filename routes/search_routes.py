from flask import Blueprint, request, jsonify 
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY') 

#blueprint for search routes
search_routes = Blueprint('search_routes', __name__)

#search route for movies, tv shows or people in one query
@search_routes.route('/search', methods=['GET'])
def search():
    query=request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    url=f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    response=requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "No movies found"}), 404
    results = response.json()
    return jsonify(results)

#search route for movies only
@search_routes.route('/search/<int:id>', methods=['GET'])
def search_movie():
    query=request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "No movies found"}), 404
    results = response.json()
    return jsonify(results)

#search route for tv shows only
@search_routes.route('/search/<int:id>', methods=['GET'])  
def search_tv_show():
    query=request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is not provided'}), 400
    url=f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={query}"
    response=requests.get(url)
    if response.status_code !=200:
        return jsonify({'error' : 'No tv shows found'})
    results = response.json()
    return jsonify(results)

