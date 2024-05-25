from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User, Meme, Comment

bp = Blueprint('admin', __name__)

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.is_admin

@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 401

    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        })

    return jsonify(result), 200

@bp.route('/admin/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@bp.route('/admin/memes', methods=['GET'])
@jwt_required()
def get_all_memes_admin():
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 401

    memes = Meme.query.all()
    result = []
    for meme in memes:
        result.append({
            'id': meme.id,
            'image_url': meme.image_url,
            'caption': meme.caption,
            'user_id': meme.user_id,
            'created_at': meme.created_at
        })

    return jsonify(result), 200

@bp.route('/admin/meme/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_meme_admin(id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 401

    meme = Meme.query.get_or_404(id)
    db.session.delete(meme)
    db.session.commit()
    return jsonify({'message': 'Meme deleted successfully'}), 200

@bp.route('/admin/meme/<int:id>', methods=['PUT'])
@jwt_required()
def update_meme_admin(id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 401

    meme = Meme.query.get_or_404(id)
    data = request.get_json()
    if data.get('caption'):
        meme.caption = data['caption']

    db.session.commit()
    return jsonify({'message': 'Meme updated successfully'}), 200
