from flask import Blueprint

categories_bp = Blueprint('categories', __name__)

from task_note_manager.app.categories import routes
