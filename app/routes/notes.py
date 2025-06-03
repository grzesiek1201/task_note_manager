"""
app/routes/notes.py
"""

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models.models import Note, db

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=['GET'])
@login_required
def get_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": n.id,
        "title": n.title,
        "content": n.content,
        "created_at": n.created_at.isoformat() if n.created_at else None,
        "updated_at": n.updated_at.isoformat() if n.updated_at else None,
        "category_id": n.category_id,
    } for n in notes])


@bp.route('/', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    if not data or not data.get('title'):
        abort(400, "Note title is required")

    note = Note(
        title=data['title'],
        content=data.get('content'),
        user_id=current_user.id,
        category_id=data.get('category_id'),
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id}), 201


@bp.route('/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    if not data:
        abort(400, "No data provided")

    for field in ['title', 'content', 'category_id']:
        if field in data:
            setattr(note, field, data[field])

    db.session.commit()
    return jsonify({"message": "Note updated"})


@bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"})
