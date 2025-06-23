import pytest
from datetime import datetime, timedelta
from app.models import User, Task, Note, Category
from app import db

def test_user_model(app):
    """Test modelu użytkownika."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
        assert str(user) == '<User testuser>'

def test_task_model(app, test_user):
    """Test modelu zadania."""
    with app.app_context():
        task = Task(
            title='Test task',
            description='Test description',
            due_date=datetime.now() + timedelta(days=1),
            priority='high',
            user=test_user
        )
        db.session.add(task)
        db.session.commit()

        assert task.id is not None
        assert task.title == 'Test task'
        assert task.description == 'Test description'
        assert task.priority == 'high'
        assert not task.completed
        assert task.user_id == test_user.id
        assert str(task) == '<Task Test task>'

def test_note_model(app, test_user):
    """Test modelu notatki."""
    with app.app_context():
        note = Note(
            title='Test note',
            content='Test content',
            user=test_user
        )
        db.session.add(note)
        db.session.commit()

        assert note.id is not None
        assert note.title == 'Test note'
        assert note.content == 'Test content'
        assert note.user_id == test_user.id
        assert str(note) == '<Note Test note>'

def test_category_model(app, test_user):
    """Test category model."""
    with app.app_context():
        category = Category(
            name='Test category',
            color='#FF0000',
            user=test_user
        )
        db.session.add(category)
        db.session.commit()

        assert category.id is not None
        assert category.name == 'Test category'
        assert category.color == '#FF0000'
        assert category.user_id == test_user.id
        assert str(category) == '<Category Test category>'

def test_task_category_relationship(app, test_user, test_categories):
    """Test relacji między zadaniem a kategorią."""
    with app.app_context():
        task = Task(
            title='Task with category',
            description='Test description',
            user=test_user,
            category=test_categories[0]
        )
        db.session.add(task)
        db.session.commit()

        assert task.category_id == test_categories[0].id
        assert task.category == test_categories[0]
        assert task in test_categories[0].tasks

def test_note_category_relationship(app, test_user, test_categories):
    """Test relacji między notatką a kategorią."""
    with app.app_context():
        note = Note(
            title='Note with category',
            content='Test content',
            user=test_user,
            category=test_categories[0]
        )
        db.session.add(note)
        db.session.commit()

        assert note.category_id == test_categories[0].id
        assert note.category == test_categories[0]
        assert note in test_categories[0].notes

def test_user_tasks_relationship(app, test_user):
    """Test relacji między użytkownikiem a zadaniami."""
    with app.app_context():
        task1 = Task(title='Task 1', user=test_user)
        task2 = Task(title='Task 2', user=test_user)
        db.session.add_all([task1, task2])
        db.session.commit()

        assert len(test_user.tasks) == 2
        assert task1 in test_user.tasks
        assert task2 in test_user.tasks

def test_user_notes_relationship(app, test_user):
    """Test relacji między użytkownikiem a notatkami."""
    with app.app_context():
        note1 = Note(title='Note 1', user=test_user)
        note2 = Note(title='Note 2', user=test_user)
        db.session.add_all([note1, note2])
        db.session.commit()

        assert len(test_user.notes) == 2
        assert note1 in test_user.notes
        assert note2 in test_user.notes

def test_user_categories_relationship(app, test_user):
    """Test relacji między użytkownikiem a kategoriami."""
    with app.app_context():
        category1 = Category(name='Category 1', user=test_user)
        category2 = Category(name='Category 2', user=test_user)
        db.session.add_all([category1, category2])
        db.session.commit()

        assert len(test_user.categories) == 2
        assert category1 in test_user.categories
        assert category2 in test_user.categories

def test_task_completion(app, test_user):
    """Test ukończenia zadania."""
    with app.app_context():
        task = Task(title='Test task', user=test_user)
        db.session.add(task)
        db.session.commit()

        assert not task.completed
        task.completed = True
        db.session.commit()

        assert task.completed
        assert task.completed_at is not None

def test_note_creation_date(app, test_user):
    """Test daty utworzenia notatki."""
    with app.app_context():
        note = Note(title='Test note', user=test_user)
        db.session.add(note)
        db.session.commit()

        assert note.created_at is not None
        assert isinstance(note.created_at, datetime) 