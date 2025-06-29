import pytest
from app.models import Note, User
from app import db

def test_notes_page(auth_client):
    """Test displaying the notes page."""
    response = auth_client.get('/notes')
    assert response.status_code == 200
    assert 'Notes' in response.data.decode('utf-8')

def test_create_note_page(auth_client):
    """Test displaying the create note page."""
    response = auth_client.get('/notes/create')
    assert response.status_code == 200
    assert 'New note' in response.data.decode('utf-8')

def test_create_note(auth_client, app, test_categories):
    """Test creating a note."""
    response = auth_client.post('/notes/create', data={
        'title': 'Test note',
        'content': 'Test content',
        'category_id': test_categories[0].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Note has been created!' in response.data.decode('utf-8')

    with app.app_context():
        note = Note.query.filter_by(title='Test note').first()
        assert note is not None
        assert note.content == 'Test content'
        assert note.category_id == test_categories[0].id

def test_edit_note_page(auth_client, test_notes):
    """Test displaying the edit note page."""
    response = auth_client.get(f'/notes/{test_notes[0].id}/edit')
    assert response.status_code == 200
    assert 'Edit note' in response.data.decode('utf-8')

def test_edit_note(auth_client, app, test_notes, test_categories):
    """Test editing a note."""
    response = auth_client.post(f'/notes/{test_notes[0].id}/edit', data={
        'title': 'Updated note',
        'content': 'Updated content',
        'category_id': test_categories[1].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Note has been updated!' in response.data.decode('utf-8')

    with app.app_context():
        note = Note.query.get(test_notes[0].id)
        assert note.title == 'Updated note'
        assert note.content == 'Updated content'
        assert note.category_id == test_categories[1].id

def test_delete_note(auth_client, app, test_notes):
    """Test deleting a note."""
    response = auth_client.post(f'/notes/{test_notes[0].id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert 'Note has been deleted!' in response.data.decode('utf-8')

    with app.app_context():
        note = Note.query.get(test_notes[0].id)
        assert note is None

def test_note_validation(auth_client, test_categories):
    """Test note data validation."""
    response = auth_client.post('/notes/create', data={
        'title': '',  # Empty field
        'content': 'Content',
        'category_id': test_categories[0].id
    })
    assert 'This field is required.' in response.data.decode('utf-8')

def test_note_access_control(auth_client, app, test_user):
    """Test note access control."""
    other_user = User(username='other', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()

    note = Note(
        title='Other user note',
        content='Content',
        user=other_user
    )
    db.session.add(note)
    db.session.commit()

    response = auth_client.get(f'/notes/{note.id}/edit')
    assert response.status_code == 404

    response = auth_client.post(f'/notes/{note.id}/delete')
    assert response.status_code == 404

def test_note_without_category(auth_client, app, test_user):
    """Test creating a note without a category."""
    response = auth_client.post('/notes/create', data={
        'title': 'Note without category',
        'content': 'Content',
        'category_id': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Note has been created!' in response.data.decode('utf-8')

    with app.app_context():
        note = Note.query.filter_by(title='Note without category').first()
        assert note is not None
        assert note.category_id is None 