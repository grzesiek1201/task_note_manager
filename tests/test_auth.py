import pytest
from flask import url_for
from app.models import User

def test_register_page(client):
    """Test registration page display."""
    response = client.get('/register')
    assert response.status_code == 200
    assert 'Registration' in response.data.decode('utf-8')

def test_register(client, app):
    """Test new user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration successful' in response.data.decode('utf-8')

    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'new@example.com'

def test_register_duplicate_username(client, test_user):
    """Test registration with existing username."""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'password',
        'password2': 'password'
    })
    assert 'Please use a different username.' in response.data.decode('utf-8')

def test_register_duplicate_email(client, test_user):
    """Test registration with existing email."""
    response = client.post('/register', data={
        'username': 'different',
        'email': 'test@example.com',
        'password': 'password',
        'password2': 'password'
    })
    assert 'Please use a different email address.' in response.data.decode('utf-8')

def test_login_page(client):
    """Test login page display."""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Login' in response.data.decode('utf-8')

def test_login(client, test_user):
    """Test user login."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode('utf-8')

def test_login_invalid_username(client):
    """Test login with invalid username."""
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'password'
    })
    assert 'Invalid username or password' in response.data.decode('utf-8')

def test_login_invalid_password(client, test_user):
    """Test login with invalid password."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert 'Invalid username or password' in response.data.decode('utf-8')

def test_logout(auth_client):
    """Test user logout."""
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'You have been logged out' in response.data.decode('utf-8')

def test_protected_route(client):
    """Test access to protected route without login."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_remember_me(client, test_user):
    """Test 'Remember me' functionality."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword',
        'remember': True
    })
    assert 'remember_token' in response.headers['Set-Cookie'] 