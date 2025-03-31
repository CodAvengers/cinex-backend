from flask import Blueprint, jsonify, request
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

favorites_bp = Blueprint('favorites', __name__)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Get the user's favorites
@favorites_bp.route('/api/favorites', methods=['GET'])
def get_favorites():
    try:
        # Get the JWT from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        # jwt = auth_header.split(' ')[1]

        # Set the JWT for the Supabase client to apply RLS
        # supabase.postgrest.auth(jwt)

        # Fetch the user's favorites (commented out until the table is created)
        # response = supabase.from_('favorites').select('*').execute()
        # favorites = response.data

        # For now, return a placeholder response
        favorites = []  # Placeholder until the table is created

        # Fetch details for each favorite from TMDb
        detailed_favorites = []
        for favorite in favorites:
            tmdb_id = favorite['tmdb_id']
            media_type = favorite['media_type']
            details_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details = details_response.json()
            detailed_favorites.append({
                "tmdb_id": tmdb_id,
                "media_type": media_type,
                "title": details.get('title', details.get('name', 'Unknown Title')),
                "poster_path": details.get('poster_path', None),
                "vote_average": details.get('vote_average', 0),
                "release_date": details.get('release_date', details.get('first_air_date', '')),
            })

        return jsonify(detailed_favorites)
    except Exception as e:
        print(f"Error fetching favorites: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Add a favorite
@favorites_bp.route('/api/favorites', methods=['POST'])
def add_favorite():
    try:
        # Get the JWT from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        # jwt = auth_header.split(' ')[1]
        # supabase.postgrest.auth(jwt)

        # Get the request data
        data = request.get_json()
        tmdb_id = data.get('tmdb_id')
        media_type = data.get('media_type')

        if not tmdb_id or not media_type or media_type not in ['movie', 'tv']:
            return jsonify({"error": "Invalid tmdb_id or media_type"}), 400

        # Insert the favorite (commented out until the table is created)
        # response = supabase.from_('favorites').insert({
        #     "tmdb_id": tmdb_id,
        #     "media_type": media_type,
        #     "user_id": supabase.auth.get_user(jwt).user.id
        # }).execute()

        return jsonify({"message": "Favorite added successfully (placeholder)"}), 201
    except Exception as e:
        print(f"Error adding favorite: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Remove a favorite
@favorites_bp.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    try:
        # Get the JWT from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        # jwt = auth_header.split(' ')[1]
        # supabase.postgrest.auth(jwt)

        # Get the request data
        data = request.get_json()
        tmdb_id = data.get('tmdb_id')
        media_type = data.get('media_type')

        if not tmdb_id or not media_type:
            return jsonify({"error": "Invalid tmdb_id or media_type"}), 400

        # Delete the favorite (commented out until the table is created)
        # response = supabase.from_('favorites').delete().eq('tmdb_id', tmdb_id).eq('media_type', media_type).execute()

        return jsonify({"message": "Favorite removed successfully (placeholder)"}), 200
    except Exception as e:
        print(f"Error removing favorite: {str(e)}")
        return jsonify({"error": str(e)}), 500