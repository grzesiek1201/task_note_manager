import pytest
from flask import url_for
from app.models import User

def test_register_page(client):
    """Test wyświetlania strony rejestracji."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Rejestracja' in response.data

def test_register(client, app):
    """Test rejestracji nowego użytkownika."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Zarejestrowano pomyślnie' in response.data

    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'new@example.com'

def test_register_duplicate_username(client, test_user):
    """Test rejestracji z istniejącą nazwą użytkownika."""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'password',
        'password2': 'password'
    })
    assert b'Użyj innej nazwy użytkownika' in response.data

def test_register_duplicate_email(client, test_user):
    """Test rejestracji z istniejącym adresem email."""
    response = client.post('/register', data={
        'username': 'different',
        'email': 'test@example.com',
        'password': 'password',
        'password2': 'password'
    })
    assert b'Użyj innego adresu email' in response.data

def test_login_page(client):
    """Test wyświetlania strony logowania."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Logowanie' in response.data

def test_login(client, test_user):
    """Test logowania użytkownika."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Witaj' in response.data

def test_login_invalid_username(client):
    """Test logowania z nieprawidłową nazwą użytkownika."""
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'password'
    })
    assert b'Nieprawidłowa nazwa użytkownika lub hasło' in response.data

def test_login_invalid_password(client, test_user):
    """Test logowania z nieprawidłowym hasłem."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert b'Nieprawidłowa nazwa użytkownika lub hasło' in response.data

def test_logout(auth_client):
    """Test wylogowania użytkownika."""
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Zostałeś wylogowany' in response.data

def test_protected_route(client):
    """Test dostępu do chronionej strony bez logowania."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_remember_me(client, test_user):
    """Test funkcji 'Zapamiętaj mnie'."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword',
        'remember': True
    })
    assert 'remember_token' in response.headers['Set-Cookie'] 