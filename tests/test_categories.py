import pytest
from app.models import Category, User
from app import db

def test_categories_page(auth_client):
    """Test displaying the categories page."""
    response = auth_client.get('/categories')
    assert response.status_code == 200
    assert 'Categories' in response.data.decode('utf-8')

def test_create_category_page(auth_client):
    """Test displaying the create category page."""
    response = auth_client.get('/categories/create')
    assert response.status_code == 200
    assert 'New category' in response.data.decode('utf-8')

def test_create_category(auth_client, app, test_user):
    """Test creating a new category."""
    response = auth_client.post('/categories/create', data={
        'name': 'New category',
        'color': '#FF0000'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Category has been created' in response.data.decode('utf-8')

    with app.app_context():
        category = Category.query.filter_by(name='New category').first()
        assert category is not None
        assert category.color == '#FF0000'
        assert category.user_id == test_user.id

def test_edit_category_page(auth_client, test_categories):
    """Test displaying the edit category page."""
    response = auth_client.get(f'/categories/{test_categories[0].id}/edit')
    assert response.status_code == 200
    assert b'Edit category' in response.data

def test_edit_category(auth_client, app, test_categories):
    """Test editing a category."""
    response = auth_client.post(f'/categories/{test_categories[0].id}/edit', data={
        'name': 'Updated category',
        'color': '#00FF00'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Category has been updated' in response.data

    with app.app_context():
        category = Category.query.get(test_categories[0].id)
        assert category.name == 'Updated category'
        assert category.color == '#00FF00'

def test_delete_category(auth_client, app, test_categories):
    """Test deleting a category."""
    response = auth_client.post(f'/categories/{test_categories[0].id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Category has been deleted' in response.data

    with app.app_context():
        category = Category.query.get(test_categories[0].id)
        assert category is None

def test_category_validation(auth_client):
    """Test category data validation."""
    response = auth_client.post('/categories/create', data={
        'name': '',  # Empty field
        'color': '#FF0000'
    })
    assert b'This field is required' in response.data

def test_category_access_control(auth_client, app, test_user):
    """Test category access control."""
    # Creating a category for another user
    other_user = User(username='other', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()

    category = Category(
        name='Foreign category',
        color='#FF0000',
        user=other_user
    )
    db.session.add(category)
    db.session.commit()

    # Attempting to edit a foreign category
    response = auth_client.get(f'/categories/{category.id}/edit')
    assert response.status_code == 404

    # Attempting to delete a foreign category
    response = auth_client.post(f'/categories/{category.id}/delete')
    assert response.status_code == 404

def test_category_with_default_color(auth_client, app, test_user):
    """Test creating a category with default color."""
    response = auth_client.post('/categories/create', data={
        'name': 'Category with default color',
        'color': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Category has been created' in response.data.decode('utf-8')

    with app.app_context():
        category = Category.query.filter_by(name='Category with default color').first()
        assert category is not None
        assert category.color == '#000000'  # Default color 