from flask import Blueprint, jsonify, request
from schemas.schemas import user_schema
from models import User,db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/api')


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

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user :  # Ensure user exists
        return jsonify({'error': 'User not found. Kindly register.'}), 401
    
    if not user.check_password(data['password']):
        return jsonify({'error': 'Incorrect password.'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user_schema.dump(user)
    }), 200
