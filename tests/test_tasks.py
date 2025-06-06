"""
tests/test_routes/test_tasks.py
"""

import pytest
from flask import url_for
from app import create_app, db
from app.models import User, Task
from flask_login import login_user
from datetime import date, datetime, timedelta
import json


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def user(app):
    user = User(username='test', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def login(client, user):
    # Manually login user using client.post
    response = client.post("/auth/login", data={
        "email": user.email,
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    return response


@pytest.fixture
def auth_headers(client, user):
    # Use login route to obtain session cookie for authentication
    client.post("/auth/login", data={
        "email": user.email,
        "password": "password"
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


def test_tasks_page(auth_client):
    """Test wyświetlania strony zadań."""
    response = auth_client.get('/tasks')
    assert response.status_code == 200
    assert b'Zadania' in response.data


def test_create_task_page(auth_client):
    """Test wyświetlania strony tworzenia zadania."""
    response = auth_client.get('/tasks/create')
    assert response.status_code == 200
    assert b'Nowe zadanie' in response.data


def test_create_task(auth_client, app, test_user, test_categories):
    """Test tworzenia nowego zadania."""
    response = auth_client.post('/tasks/create', data={
        'title': 'Nowe zadanie',
        'description': 'Opis nowego zadania',
        'due_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        'priority': 'high',
        'category_id': test_categories[0].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Zadanie zostało utworzone' in response.data

    with app.app_context():
        task = Task.query.filter_by(title='Nowe zadanie').first()
        assert task is not None
        assert task.description == 'Opis nowego zadania'
        assert task.priority == 'high'
        assert task.category_id == test_categories[0].id


def test_edit_task_page(auth_client, test_tasks):
    """Test wyświetlania strony edycji zadania."""
    response = auth_client.get(f'/tasks/{test_tasks[0].id}/edit')
    assert response.status_code == 200
    assert b'Edycja zadania' in response.data


def test_edit_task(auth_client, app, test_tasks, test_categories):
    """Test edycji zadania."""
    response = auth_client.post(f'/tasks/{test_tasks[0].id}/edit', data={
        'title': 'Zaktualizowane zadanie',
        'description': 'Zaktualizowany opis',
        'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
        'priority': 'medium',
        'category_id': test_categories[1].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Zadanie zostało zaktualizowane' in response.data

    with app.app_context():
        task = Task.query.get(test_tasks[0].id)
        assert task.title == 'Zaktualizowane zadanie'
        assert task.description == 'Zaktualizowany opis'
        assert task.priority == 'medium'
        assert task.category_id == test_categories[1].id


def test_delete_task(auth_client, app, test_tasks):
    """Test usuwania zadania."""
    response = auth_client.post(f'/tasks/{test_tasks[0].id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Zadanie zostało usunięte' in response.data

    with app.app_context():
        task = Task.query.get(test_tasks[0].id)
        assert task is None


def test_toggle_task(auth_client, app, test_tasks):
    """Test przełączania statusu zadania."""
    response = auth_client.post(f'/tasks/{test_tasks[0].id}/toggle', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = Task.query.get(test_tasks[0].id)
        assert task.completed is True


def test_task_validation(auth_client, test_categories):
    """Test walidacji danych zadania."""
    response = auth_client.post('/tasks/create', data={
        'title': '',  # Puste pole
        'description': 'Opis',
        'due_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        'priority': 'high',
        'category_id': test_categories[0].id
    })
    assert b'To pole jest wymagane' in response.data


def test_task_access_control(auth_client, app, test_user):
    """Test kontroli dostępu do zadań."""
    # Tworzenie zadania dla innego użytkownika
    other_user = User(username='other', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()

    task = Task(
        title='Cudze zadanie',
        description='Opis',
        user=other_user
    )
    db.session.add(task)
    db.session.commit()

    # Próba edycji cudzego zadania
    response = auth_client.get(f'/tasks/{task.id}/edit')
    assert response.status_code == 404

    # Próba usunięcia cudzego zadania
    response = auth_client.post(f'/tasks/{task.id}/delete')
    assert response.status_code == 404
