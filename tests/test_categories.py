import pytest
from app.models import Category, User
from app import db

def test_categories_page(auth_client):
    """Test wyświetlania strony kategorii."""
    response = auth_client.get('/categories')
    assert response.status_code == 200
    assert b'Kategorie' in response.data

def test_create_category_page(auth_client):
    """Test wyświetlania strony tworzenia kategorii."""
    response = auth_client.get('/categories/create')
    assert response.status_code == 200
    assert b'Nowa kategoria' in response.data

def test_create_category(auth_client, app, test_user):
    """Test tworzenia nowej kategorii."""
    response = auth_client.post('/categories/create', data={
        'name': 'Nowa kategoria',
        'color': '#FF0000'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Kategoria została utworzona' in response.data

    with app.app_context():
        category = Category.query.filter_by(name='Nowa kategoria').first()
        assert category is not None
        assert category.color == '#FF0000'
        assert category.user_id == test_user.id

def test_edit_category_page(auth_client, test_categories):
    """Test wyświetlania strony edycji kategorii."""
    response = auth_client.get(f'/categories/{test_categories[0].id}/edit')
    assert response.status_code == 200
    assert b'Edycja kategorii' in response.data

def test_edit_category(auth_client, app, test_categories):
    """Test edycji kategorii."""
    response = auth_client.post(f'/categories/{test_categories[0].id}/edit', data={
        'name': 'Zaktualizowana kategoria',
        'color': '#00FF00'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Kategoria została zaktualizowana' in response.data

    with app.app_context():
        category = Category.query.get(test_categories[0].id)
        assert category.name == 'Zaktualizowana kategoria'
        assert category.color == '#00FF00'

def test_delete_category(auth_client, app, test_categories):
    """Test usuwania kategorii."""
    response = auth_client.post(f'/categories/{test_categories[0].id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Kategoria została usunięta' in response.data

    with app.app_context():
        category = Category.query.get(test_categories[0].id)
        assert category is None

def test_category_validation(auth_client):
    """Test walidacji danych kategorii."""
    response = auth_client.post('/categories/create', data={
        'name': '',  # Puste pole
        'color': '#FF0000'
    })
    assert b'To pole jest wymagane' in response.data

def test_category_access_control(auth_client, app, test_user):
    """Test kontroli dostępu do kategorii."""
    # Tworzenie kategorii dla innego użytkownika
    other_user = User(username='other', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()

    category = Category(
        name='Cudza kategoria',
        color='#FF0000',
        user=other_user
    )
    db.session.add(category)
    db.session.commit()

    # Próba edycji cudzej kategorii
    response = auth_client.get(f'/categories/{category.id}/edit')
    assert response.status_code == 404

    # Próba usunięcia cudzej kategorii
    response = auth_client.post(f'/categories/{category.id}/delete')
    assert response.status_code == 404

def test_category_with_default_color(auth_client, app, test_user):
    """Test tworzenia kategorii z domyślnym kolorem."""
    response = auth_client.post('/categories/create', data={
        'name': 'Kategoria z domyślnym kolorem',
        'color': ''  # Puste pole koloru
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Kategoria została utworzona' in response.data

    with app.app_context():
        category = Category.query.filter_by(name='Kategoria z domyślnym kolorem').first()
        assert category is not None
        assert category.color == '#000000'  # Domyślny kolor 