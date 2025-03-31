from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

trending_routes = Blueprint('trending_routes', __name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@trending_routes.route('/trending/movies', methods=['GET'])
def get_trending_movies():
    try:
        # Get trending movies from TMDB (daily trend)
        response = requests.get(
            f"{BASE_URL}/trending/movie/day",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        response.raise_for_status()
        
        # Process the results
        trending_movies = []
        for movie in response.json()['results'][:20]:  # Get top 20 trending
            trending_movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                'vote_average': movie['vote_average'],
                'release_date': movie['release_date'],
                'popularity': movie['popularity'],
                'trending_rank': len(trending_movies) + 1  # Add ranking position
            })
        
        return jsonify({
            'success': True,
            'time_window': 'day',  # Can be changed to 'week'
            'results': trending_movies
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


#get te trending series
@trending_routes.route('trending/series', methods=['GET'])
def get_trending_series():
    #dynamically change the page from reequest or default to one
    page = request.args.get('page', '1')
    url = f'{BASE_URL}/trending/tv/day?page={page}&language=en-US'
    headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status() #get the returned status code

    if response.status_code != 200:
        return jsonify({'error': 'No popular movies found'}), 400

    series_list =[]
    #loopthrough the results
    for series in response.json()['results']:
        series_list.append({
            'id': series['id'],
            'name': series['name'],
            'overview': series['overview'],
            'poster_path': f"https://image.tmdb.org/t/p/w500{series['poster_path']}" if series['poster_path'] else None,
            'rating': series['vote_average'],
            'first_air_date': series['first_air_date'],
            'media_type': 'tv'
        })
    return jsonify({'succes': True, 'results': series_list})
