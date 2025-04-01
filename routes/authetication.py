from flask import Blueprint, jsonify, request
from schemas.schemas import user_schema
from models import User,db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400


    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Create new user instance
    new_user = User(
        email=data['email']
    )
    new_user.set_password(data['password'])  # Use set_password method to hash the password

    # Save user to database
    db.session.add(new_user)
    db.session.commit()

    # Generate access token
    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        'message': 'User added successfully',
        'token': access_token,
        'user': user_schema.dump(new_user)
    }), 201
