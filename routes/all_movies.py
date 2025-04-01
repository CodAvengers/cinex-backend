import requests
import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
load_dotenv()

#base url and importing appi key
base_url = "https://api.themoviedb.org/3"
tmb_api_key = os.getenv('TMDB_API_KEY')

#initiallising the blueprint
all_movies = Blueprint('all_movies', __name__, url_prefix='/api')

#route to return discover all movies
@all_movies.route('/movies', methods=['GET'])
def get_all_movies():
    #dynamically set the page to be determined from the qurry parameter or default to one
    page = request.args.get('page','1')  
    url = f"{base_url}/discover/movie?include_adult=false&language=en-US&page={page}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmb_api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error:", response.text)
        return jsonify({'error': 'No popular movies found'}), 400
    movies = []
    for movie in response.json()['results']: #loop through each reult in results
        movies.append({
            'id': movie['id'],
            'title': movie['title'],
            'overview': movie['overview'],
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
            'rating': movie['vote_average'],
            'release_date': movie['release_date'],
            'media_type': 'movie',
        })
    
    return jsonify({'success': True, 'results': movies})

#route to return discover all tv shows
@all_movies.route('/series', methods=['GET'])
def get_all_series():
     #dynamically set the page to be determined from the qurry parameter or default to one
    page = request.args.get('page', '1')
    url = f"{base_url}/discover/tv?include_adult=false&language=en-US&page={page}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmb_api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error:", response.text)
        return jsonify({'error': 'No popular movies found'}), 400
    series = []
    for show in response.json()['results']: #loop through each reult in results
        series.append({
            'id': show['id'],
            'name': show['name'],
            'overview': show['overview'],
            'poster_path': f"https://image.tmdb.org/t/p/w500{show['poster_path']}" if show['poster_path'] else None,
            'rating': show['vote_average'],
            'first_air_date': show['first_air_date'],
            'media_type': 'tv',
        })
    
    return jsonify({'success': True, 'results': series})
