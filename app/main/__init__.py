from flask import Blueprint

main_bp = Blueprint('main', __name__)

from task_note_manager.app.main import routes
