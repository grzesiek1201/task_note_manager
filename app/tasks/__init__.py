from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__)

from task_note_manager.app.tasks import routes
