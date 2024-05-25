from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Like, Comment

bp = Blueprint('interactions', __name__)

@bp.route('/like/<int:meme_id>', methods=['POST'])
@jwt_required()
def like_meme(meme_id):
    user_id = get_jwt_identity()

    like = Like.query.filter_by(user_id=user_id, meme_id=meme_id).first()
    if like:
        return jsonify({'message': 'Already liked'}), 400

    new_like = Like(user_id=user_id, meme_id=meme_id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({'message': 'Meme liked successfully'}), 201

@bp.route('/unlike/<int:meme_id>', methods=['DELETE'])
@jwt_required()
def unlike_meme(meme_id):
    user_id = get_jwt_identity()

    like = Like.query.filter_by(user_id=user_id, meme_id=meme_id).first()
    if not like:
        return jsonify({'message': 'Not liked yet'}), 400

    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Meme unliked successfully'}), 200

@bp.route('/comment/<int:meme_id>', methods=['POST'])
@jwt_required()
def comment_on_meme(meme_id):
    user_id = get_jwt_identity()

    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'message': 'Invalid data'}), 400

    new_comment = Comment(
        user_id=user_id,
        meme_id=meme_id,
        content=data['content']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

@bp.route('/comment/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    user_id = get_jwt_identity()

    comment = Comment.query.get_or_404(id)
    if comment.user_id != user_id:
        return jsonify({'message': 'Forbidden'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200

@bp.route('/comments/<int:meme_id>', methods=['GET'])
def get_comments(meme_id):
    comments = Comment.query.filter_by(meme_id=meme_id).all()
    result = []
    for comment in comments:
        result.append({
            'id': comment.id,
            'user_id': comment.user_id,
            'content': comment.content,
            'created_at': comment.created_at
        })

    return jsonify(result), 200
