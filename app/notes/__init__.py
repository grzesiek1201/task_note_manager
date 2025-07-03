from flask import Blueprint

notes_bp = Blueprint('notes', __name__)

from task_note_manager.app.notes import routes
