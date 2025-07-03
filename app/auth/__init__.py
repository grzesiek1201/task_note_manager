from flask import Blueprint


auth_bp = Blueprint('auth', __name__)

from task_note_manager.app.auth import routes
