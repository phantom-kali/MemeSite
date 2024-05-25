from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User
import re

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid data'}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at
    }), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(user_id)

    if data.get('username'):
        user.username = data['username']
    if data.get('email'):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 400
        user.email = data['email']
    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200
