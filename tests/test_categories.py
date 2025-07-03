import pytest
from task_note_manager.app.models.models import Category

def test_create_category(auth_client, app):
    response = auth_client.post('/categories/create', data={
        'name': 'Test Category',
        'description': 'Test description'
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Category has been created!' in html
    with app.app_context():
        category = Category.query.filter_by(name='Test Category').first()
        assert category is not None

def test_edit_category(auth_client, test_categories, app):
    category = test_categories[0]
    response = auth_client.post(f'/categories/{category.id}/edit', data={
        'name': 'Updated Category',
        'description': 'Updated description'
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Category has been updated!' in html
    with app.app_context():
        updated = Category.query.get(category.id)
        assert updated.name == 'Updated Category'

def test_delete_category(auth_client, test_categories, app):
    category = test_categories[0]
    response = auth_client.post(f'/categories/{category.id}/delete', follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Category has been deleted!' in html
    with app.app_context():
        deleted = Category.query.get(category.id)
        assert deleted is None

def test_list_categories(auth_client):
    response = auth_client.get('/categories')
    html = response.data.decode('utf-8')
    print(html)
    assert 'Work' in html or 'Home' in html or 'Hobby' in html 