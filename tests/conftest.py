import pytest
from app import create_app, db
from app.models import User, Task, Note, Category
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Tworzy instancję aplikacji do testów."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Tworzy klienta testowego."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Tworzy runner CLI do testów."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Tworzy użytkownika testowego."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_client(client, test_user):
    """Tworzy zalogowanego klienta testowego."""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    return client

@pytest.fixture
def test_categories(app, test_user):
    """Tworzy kategorie testowe."""
    categories = [
        Category(name='Praca', color='#FF0000', user=test_user),
        Category(name='Dom', color='#00FF00', user=test_user),
        Category(name='Hobby', color='#0000FF', user=test_user)
    ]
    for category in categories:
        db.session.add(category)
    db.session.commit()
    return categories

@pytest.fixture
def test_tasks(app, test_user, test_categories):
    """Tworzy zadania testowe."""
    tasks = [
        Task(
            title='Zadanie 1',
            description='Opis zadania 1',
            due_date=datetime.now() + timedelta(days=1),
            priority='high',
            category=test_categories[0],
            user=test_user
        ),
        Task(
            title='Zadanie 2',
            description='Opis zadania 2',
            due_date=datetime.now() + timedelta(days=2),
            priority='medium',
            category=test_categories[1],
            user=test_user
        ),
        Task(
            title='Zadanie 3',
            description='Opis zadania 3',
            due_date=datetime.now() + timedelta(days=3),
            priority='low',
            category=test_categories[2],
            user=test_user
        )
    ]
    for task in tasks:
        db.session.add(task)
    db.session.commit()
    return tasks

@pytest.fixture
def test_notes(app, test_user, test_categories):
    """Tworzy notatki testowe."""
    notes = [
        Note(
            title='Notatka 1',
            content='Treść notatki 1',
            category=test_categories[0],
            user=test_user
        ),
        Note(
            title='Notatka 2',
            content='Treść notatki 2',
            category=test_categories[1],
            user=test_user
        ),
        Note(
            title='Notatka 3',
            content='Treść notatki 3',
            category=test_categories[2],
            user=test_user
        )
    ]
    for note in notes:
        db.session.add(note)
    db.session.commit()
    return notes 