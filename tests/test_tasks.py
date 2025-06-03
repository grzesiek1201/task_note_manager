"""
tests/test_routes/test_tasks.py
"""

import pytest
from app import create_app, db
from app.models.models import User, Task
from flask_login import login_user
from datetime import date, datetime
import json


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def login(client, user):
    # Manually login user using client.post
    response = client.post("/auth/login", data={
        "email": user.email,
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    return response


@pytest.fixture
def auth_headers(client, user):
    # Use login route to obtain session cookie for authentication
    client.post("/auth/login", data={
        "email": user.email,
        "password": "password123"
    }, follow_redirects=True)
    return {}


def test_get_tasks_empty(client, user, auth_headers):
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert response.is_json
    assert response.json == []


def test_create_task_missing_title(client, user, auth_headers):
    response = client.post("/tasks/", json={}, headers=auth_headers)
    assert response.status_code == 400
    assert b"Title is required" in response.data


def test_create_and_get_task(client, user, auth_headers):
    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "due_date": "2025-06-10",
        "category_id": None,
    }
    post_resp = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert post_resp.status_code == 201
    task_id = post_resp.json["id"]
    assert isinstance(task_id, int)

    get_resp = client.get("/tasks/", headers=auth_headers)
    assert get_resp.status_code == 200
    tasks = get_resp.json
    assert len(tasks) == 1
    task = tasks[0]
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]
    assert task["description"] == task_data["description"]
    assert task["due_date"] == task_data["due_date"]
    assert task["completed"] is False


def test_update_task(client, user, auth_headers):
    # Create a task first
    task = Task(title="Old title", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    update_data = {
        "title": "New title",
        "completed": True,
        "due_date": "2025-07-01",
    }
    resp = client.put(f"/tasks/{task.id}", json=update_data, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json["message"] == "Task updated"

    updated_task = Task.query.get(task.id)
    assert updated_task.title == update_data["title"]
    assert updated_task.completed is True
    assert updated_task.due_date == datetime.fromisoformat(update_data["due_date"]).date()


def test_update_task_invalid_date(client, user, auth_headers):
    task = Task(title="Test", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    resp = client.put(f"/tasks/{task.id}", json={"due_date": "invalid-date"}, headers=auth_headers)
    assert resp.status_code == 400
    assert b"Invalid due_date format" in resp.data


def test_delete_task(client, user, auth_headers):
    task = Task(title="Task to delete", user_id=user.id)
    db.session.add(task)
    db.session.commit()

    resp = client.delete(f"/tasks/{task.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json["message"] == "Task deleted"

    deleted_task = Task.query.get(task.id)
    assert deleted_task is None


def test_delete_task_not_found(client, user, auth_headers):
    resp = client.delete("/tasks/99999", headers=auth_headers)
    assert resp.status_code == 404
