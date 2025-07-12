import pytest
from app.models.models import Note

def test_create_note(auth_client, test_categories, app):
    response = auth_client.post('/notes/create', data={
        'title': 'Test Note',
        'content': 'Test content',
        'category_id': test_categories[0].id
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Note has been created!' in html
    with app.app_context():
        note = Note.query.filter_by(title='Test Note').first()
        assert note is not None

def test_edit_note(auth_client, test_notes, app):
    note = test_notes[0]
    response = auth_client.post(f'/notes/{note.id}/edit', data={
        'title': 'Updated Note',
        'content': 'Updated content',
        'category_id': note.category_id
    }, follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Note has been updated!' in html
    with app.app_context():
        updated = Note.query.get(note.id)
        assert updated.title == 'Updated Note'

def test_delete_note(auth_client, test_notes, app):
    note = test_notes[0]
    response = auth_client.post(f'/notes/{note.id}/delete', follow_redirects=True)
    html = response.data.decode('utf-8')
    print(html)
    assert 'Note has been deleted!' in html
    with app.app_context():
        deleted = Note.query.get(note.id)
        assert deleted is None

def test_list_notes(auth_client):
    response = auth_client.get('/notes')
    html = response.data.decode('utf-8')
    print(html)
    assert 'Note' in html 