import pytest
from task_note_manager.app.models.models import User
from flask import url_for

def test_register(client, app):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Congratulations, registration was successful!' in html
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'

def test_login_logout(client, test_user):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Welcome!' in html
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out' in response.data

def test_login_wrong_password(client, test_user):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Invalid username or password' in html 