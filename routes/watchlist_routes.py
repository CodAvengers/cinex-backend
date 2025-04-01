from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Watchlist

watchlist_routes = Blueprint('watchlist_routes', __name__, url_prefix='/api')

@watchlist_routes.route('/watchlist/add', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    try:
        # Get current user from JWT
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Get data from request
        data = request.get_json()
        tmdb_id = data.get('tmdb_id')
        
        if not tmdb_id:
            return jsonify({'success': False, 'error': 'TMDB ID is required'}), 400

        # Check if already in watchlist
        existing = Watchlist.query.filter_by(
            user_id=user.id,
            tmdb_id=tmdb_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Movie already in watchlist'
            }), 409

        # Add to watchlist
        new_watchlist_item = Watchlist(
            user_id=user.id,
            tmdb_id=tmdb_id
        )
        
        db.session.add(new_watchlist_item)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Added to watchlist',
            'watchlist_id': new_watchlist_item.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to add to watchlist',
            'details': str(e)
        }), 500

# Get User's Watchlist    
@watchlist_routes.route('/watchlist', methods=['GET'])
@jwt_required()
def get_watchlist():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        watchlist_items = Watchlist.query.filter_by(user_id=user.id).all()
        
        return jsonify({
            'success': True,
            'count': len(watchlist_items),
            'results': [{
                'id': item.id,
                'tmdb_id': item.tmdb_id,
                'added_at': item.added_at.isoformat() if hasattr(item, 'added_at') else None
            } for item in watchlist_items]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch watchlist',
            'details': str(e)
        }), 500

#Remove from Watchlist 
@watchlist_routes.route('/watchlist/remove/<int:tmdb_id>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(tmdb_id):
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        item = Watchlist.query.filter_by(
            user_id=user.id,
            tmdb_id=tmdb_id
        ).first()
        
        if not item:
            return jsonify({
                'success': False,
                'error': 'Item not in watchlist'
            }), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Removed from watchlist'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to remove from watchlist',
            'details': str(e)
        }), 500

