import pytest
from app.models import Note, User
from app import db

def test_notes_page(auth_client):
    """Test wyświetlania strony notatek."""
    response = auth_client.get('/notes')
    assert response.status_code == 200
    assert b'Notatki' in response.data

def test_create_note_page(auth_client):
    """Test wyświetlania strony tworzenia notatki."""
    response = auth_client.get('/notes/create')
    assert response.status_code == 200
    assert b'Nowa notatka' in response.data

def test_create_note(auth_client, app, test_user, test_categories):
    """Test tworzenia nowej notatki."""
    response = auth_client.post('/notes/create', data={
        'title': 'Nowa notatka',
        'content': 'Treść nowej notatki',
        'category_id': test_categories[0].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Notatka została utworzona' in response.data

    with app.app_context():
        note = Note.query.filter_by(title='Nowa notatka').first()
        assert note is not None
        assert note.content == 'Treść nowej notatki'
        assert note.category_id == test_categories[0].id

def test_edit_note_page(auth_client, test_notes):
    """Test wyświetlania strony edycji notatki."""
    response = auth_client.get(f'/notes/{test_notes[0].id}/edit')
    assert response.status_code == 200
    assert b'Edycja notatki' in response.data

def test_edit_note(auth_client, app, test_notes, test_categories):
    """Test edycji notatki."""
    response = auth_client.post(f'/notes/{test_notes[0].id}/edit', data={
        'title': 'Zaktualizowana notatka',
        'content': 'Zaktualizowana treść',
        'category_id': test_categories[1].id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Notatka została zaktualizowana' in response.data

    with app.app_context():
        note = Note.query.get(test_notes[0].id)
        assert note.title == 'Zaktualizowana notatka'
        assert note.content == 'Zaktualizowana treść'
        assert note.category_id == test_categories[1].id

def test_delete_note(auth_client, app, test_notes):
    """Test usuwania notatki."""
    response = auth_client.post(f'/notes/{test_notes[0].id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Notatka została usunięta' in response.data

    with app.app_context():
        note = Note.query.get(test_notes[0].id)
        assert note is None

def test_note_validation(auth_client, test_categories):
    """Test walidacji danych notatki."""
    response = auth_client.post('/notes/create', data={
        'title': '',  # Puste pole
        'content': 'Treść',
        'category_id': test_categories[0].id
    })
    assert b'To pole jest wymagane' in response.data

def test_note_access_control(auth_client, app, test_user):
    """Test kontroli dostępu do notatek."""
    # Tworzenie notatki dla innego użytkownika
    other_user = User(username='other', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()

    note = Note(
        title='Cudza notatka',
        content='Treść',
        user=other_user
    )
    db.session.add(note)
    db.session.commit()

    # Próba edycji cudzej notatki
    response = auth_client.get(f'/notes/{note.id}/edit')
    assert response.status_code == 404

    # Próba usunięcia cudzej notatki
    response = auth_client.post(f'/notes/{note.id}/delete')
    assert response.status_code == 404

def test_note_without_category(auth_client, app, test_user):
    """Test tworzenia notatki bez kategorii."""
    response = auth_client.post('/notes/create', data={
        'title': 'Notatka bez kategorii',
        'content': 'Treść',
        'category_id': ''  # Puste pole kategorii
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Notatka została utworzona' in response.data

    with app.app_context():
        note = Note.query.filter_by(title='Notatka bez kategorii').first()
        assert note is not None
        assert note.category_id is None 