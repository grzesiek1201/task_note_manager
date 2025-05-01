"""
categories.py
"""
from flask import Blueprint

bp = Blueprint('categories', __name__)


@bp.route('/categories')
def tasks():
    return "Categories Page"
