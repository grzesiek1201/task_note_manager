"""
app/routes/tasks.py
"""

from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from app.models.models import Task, db
from datetime import datetime

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def parse_due_date(date_str):
    if not date_str:
        return None
    try:
        # date format: YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(400, description="Invalid due_date format. Expected YYYY-MM-DD.")


@bp.route("/", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "completed": t.completed,
        "category_id": t.category_id,
    } for t in tasks])


@bp.route("/", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        abort(400, "Title is required")

    due_date = parse_due_date(data.get("due_date"))

    task = Task(
        title=data["title"],
        description=data.get("description"),
        due_date=due_date,
        completed=False,
        user_id=current_user.id,
        category_id=data.get("category_id"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id}), 201


@bp.route("/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    if not data:
        abort(400, "No data provided")

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "due_date" in data:
        task.due_date = parse_due_date(data["due_date"])
    if "completed" in data:
        if isinstance(data["completed"], bool):
            task.completed = data["completed"]
        else:
            abort(400, "Completed must be a boolean")
    if "category_id" in data:
        task.category_id = data["category_id"]

    db.session.commit()
    return jsonify({"message": "Task updated"})


@bp.route("/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
