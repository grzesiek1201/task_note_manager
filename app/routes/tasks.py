"""
tasks.py
"""
from flask import Blueprint

bp = Blueprint('tasks', __name__)


@bp.route('/tasks')
def tasks():
    return "Tasks Page"
