"""
notes.py
"""

from flask import Blueprint

bp = Blueprint('notes', __name__)


@bp.route('/notes')
def tasks():
    return "Notes Page"
