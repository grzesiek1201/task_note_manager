import pytest
from app.models.models import Task

def test_create_task(auth_client, test_categories, app):
    response = auth_client.post('/tasks/create', data={
        'title': 'Test Task',
        'description': 'Test description',
        'due_date': '2030-01-01T12:00',
        'priority': 'high',
        'category_id': test_categories[0].id
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Task has been created!' in html
    with app.app_context():
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None

def test_edit_task(auth_client, test_tasks, app):
    task = test_tasks[0]
    response = auth_client.post(f'/tasks/{task.id}/edit', data={
        'title': 'Updated Task',
        'description': 'Updated description',
        'due_date': '2030-01-02T12:00',
        'priority': 'medium',
        'category_id': task.category_id
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Task has been updated!' in html
    with app.app_context():
        updated = Task.query.get(task.id)
        assert updated.title == 'Updated Task'

def test_delete_task(auth_client, test_tasks, app):
    task = test_tasks[0]
    response = auth_client.post(f'/tasks/{task.id}/delete', follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Task has been deleted!' in html
    with app.app_context():
        deleted = Task.query.get(task.id)
        assert deleted is None

def test_toggle_task(auth_client, test_tasks, app):
    task = test_tasks[0]
    response = auth_client.post(f'/tasks/{task.id}/toggle', follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Task status has been updated!' in html
    with app.app_context():
        toggled = Task.query.get(task.id)
        assert toggled.completed is True

def test_list_tasks(auth_client):
    response = auth_client.get('/tasks')
    html = response.data.decode('utf-8')
    print(html)
    assert 'Task' in html 