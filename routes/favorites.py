from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv
from models import Favourite, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Load environment variables
load_dotenv()

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api')

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Get the user's favorites
@favorites_bp.route('/favorites', methods=['GET'])
@jwt_required()  # Require JWT authentication
def get_favorites():
    try:
        # Get the current user's ID from the JWT
        user_id = get_jwt_identity()

        # Fetch the user's favorites from the database
        favorites = Favourite.query.filter_by(user_id=user_id).all()

        # Fetch details for each favorite from TMDb
        detailed_favorites = []
        for favorite in favorites:
            tmdb_id = favorite.tmdb_id

            # Determine if the tmdb_id refers to a movie or series
            # First, try as a movie
            movie_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
            movie_response = requests.get(movie_details_url)
            if movie_response.status_code == 200:
                media_type = 'movie'
                details = movie_response.json()
            else:
                # If not a movie, try as a series
                series_details_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
                series_response = requests.get(series_details_url)
                series_response.raise_for_status()
                media_type = 'tv'
                details = series_response.json()

            detailed_favorites.append({
                "tmdb_id": tmdb_id,
                "media_type": media_type,
                "title": details.get('title', details.get('name', 'Unknown Title')),
                "poster_path": details.get('poster_path', None),
                "vote_average": details.get('vote_average', 0),
                "release_date": details.get('release_date', details.get('first_air_date', '')),
            })

        return jsonify(detailed_favorites), 200
    except Exception as e:
        print(f"Error fetching favorites: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Add a favorite
@favorites_bp.route('/favorites', methods=['POST'])
@jwt_required()  # Require JWT authentication
def add_favorite():
    try:
        # Get the current user's ID from the JWT
        user_id = get_jwt_identity()

        # Get the request data
        data = request.get_json()
        tmdb_id = data.get('tmdb_id')

        if not tmdb_id:
            return jsonify({"error": "Missing tmdb_id"}), 400

        # Check if the favorite already exists for this user
        existing_favorite = Favourite.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
        if existing_favorite:
            return jsonify({"error": "This item is already in your favorites"}), 400

        # Create a new favorite
        new_favorite = Favourite(
            user_id=user_id,
            tmdb_id=tmdb_id
        )

        # Save to the database
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"message": "Favorite added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding favorite: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Remove a favorite
@favorites_bp.route('/favorites', methods=['DELETE'])
@jwt_required()  # Require JWT authentication
def remove_favorite():
    try:
        # Get the current user's ID from the JWT
        user_id = get_jwt_identity()

        # Get the request data
        data = request.get_json()
        tmdb_id = data.get('tmdb_id')

        if not tmdb_id:
            return jsonify({"error": "Missing tmdb_id"}), 400

        # Find the favorite to delete
        favorite = Favourite.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        # Delete the favorite
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error removing favorite: {str(e)}")
        return jsonify({"error": str(e)}), 500