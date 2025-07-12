import pytest
from app import create_app, db
from app.models.models import User, Task, Note, Category
from config import Config
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Create a Flask application instance for testing.
    
    Returns:
        Flask: Configured Flask application for testing.
    """
    app = create_app(Config)
    app.config['WTF_CSRF_ENABLED'] = False  # Wyłącz CSRF w testach
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the application.
    
    Args:
        app: Flask application instance.
        
    Returns:
        FlaskClient: Test client for making requests.
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a CLI runner for testing.
    
    Args:
        app: Flask application instance.
        
    Returns:
        FlaskCliRunner: CLI runner for testing commands.
    """
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user for testing.
    
    Args:
        app: Flask application instance.
        
    Returns:
        User: Test user instance.
    """
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_client(client, test_user):
    """Create an authenticated test client.
    
    Args:
        client: Test client instance.
        test_user: Test user instance.
        
    Returns:
        FlaskClient: Authenticated test client.
    """
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    client.post('/login', data=login_data, follow_redirects=True)
    return client

@pytest.fixture
def test_categories(app, test_user):
    """Create test categories for testing.
    
    Args:
        app: Flask application instance.
        test_user: Test user instance.
        
    Returns:
        list: List of test category instances.
    """
    categories = [
        Category(name='Work', color='#FF0000', user=test_user),
        Category(name='Home', color='#00FF00', user=test_user),
        Category(name='Hobby', color='#0000FF', user=test_user)
    ]
    for category in categories:
        db.session.add(category)
    db.session.commit()
    return categories

@pytest.fixture
def test_tasks(app, test_user, test_categories):
    """Create test tasks for testing.
    
    Args:
        app: Flask application instance.
        test_user: Test user instance.
        test_categories: List of test category instances.
        
    Returns:
        list: List of test task instances.
    """
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
    """Create test notes for testing.
    
    Args:
        app: Flask application instance.
        test_user: Test user instance.
        test_categories: List of test category instances.
        
    Returns:
        list: List of test note instances.
    """
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