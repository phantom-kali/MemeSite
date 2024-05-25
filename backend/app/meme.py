from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from .models import db, Meme

bp = Blueprint('meme', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_meme():
    user_id = get_jwt_identity()

    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_meme = Meme(
            image_url=filepath,
            caption=request.form.get('caption', ''),
            user_id=user_id
        )
        db.session.add(new_meme)
        db.session.commit()

        return jsonify({'message': 'Meme uploaded successfully'}), 201

    return jsonify({'message': 'File type not allowed'}), 400

@bp.route('/memes', methods=['GET'])
def get_all_memes():
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

@bp.route('/meme/<int:id>', methods=['GET'])
def get_meme(id):
    meme = Meme.query.get_or_404(id)
    return jsonify({
        'id': meme.id,
        'image_url': meme.image_url,
        'caption': meme.caption,
        'user_id': meme.user_id,
        'created_at': meme.created_at
    }), 200

@bp.route('/meme/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_meme(id):
    user_id = get_jwt_identity()
    meme = Meme.query.get_or_404(id)
    if meme.user_id != user_id:
        return jsonify({'message': 'Forbidden'}), 403

    db.session.delete(meme)
    db.session.commit()
    return jsonify({'message': 'Meme deleted successfully'}), 200

@bp.route('/meme/<int:id>', methods=['PUT'])
@jwt_required()
def update_meme(id):
    user_id = get_jwt_identity()
    meme = Meme.query.get_or_404(id)
    if meme.user_id != user_id:
        return jsonify({'message': 'Forbidden'}), 403

    data = request.get_json()
    if data.get('caption'):
        meme.caption = data['caption']

    db.session.commit()
    return jsonify({'message': 'Meme updated successfully'}), 200
