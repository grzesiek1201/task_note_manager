"""
app/routes/categories.py
"""

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models.models import Category, db

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('/', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "description": c.description
    } for c in categories])


@bp.route('/', methods=['POST'])
@login_required
def create_category():
    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, "Category name is required")

    existing = Category.query.filter_by(name=data['name'], user_id=current_user.id).first()
    if existing:
        abort(400, "Category with this name already exists")

    category = Category(
        name=data['name'],
        description=data.get('description'),
        user_id=current_user.id
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": category.id}), 201


@bp.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    if not data:
        abort(400, "No data provided")

    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    db.session.commit()
    return jsonify({"message": "Category updated"})


@bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"})
