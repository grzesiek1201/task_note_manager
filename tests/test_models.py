import pytest
from task_note_manager.app.models.models import User, Task, Note, Category
from datetime import datetime

def test_user_password():
    user = User(username='user', email='user@example.com')
    user.set_password('strongpassword')
    assert user.check_password('strongpassword')
    assert not user.check_password('wrongpassword')

def test_task_mark_done():
    task = Task(title='t', user_id=1)
    assert not task.completed
    task.mark_done()
    assert task.completed
    assert isinstance(task.updated_at, datetime)

def test_as_dict_methods():
    user = User(id=1, username='u', email='e@example.com')
    category = Category(id=1, name='c', user_id=1)
    note = Note(id=1, title='n', content='c', user_id=1, category_id=1)
    task = Task(id=1, title='t', user_id=1, category_id=1)
    assert isinstance(user.as_dict(), dict)
    assert isinstance(category.as_dict(), dict)
    assert isinstance(note.as_dict(), dict)
    assert isinstance(task.as_dict(), dict) 