"""
Script for testing database connection.
"""

from app import create_app, db
from app.models import User, Task, Category
from datetime import datetime, timedelta

def test_database():
    app = create_app()
    with app.app_context():
        # Create test user
        test_user = User(username='test_user', email='test@example.com')
        test_user.set_password('test_password')
        db.session.add(test_user)
        db.session.commit()

        # Create test categories
        categories = [
            Category(name='Work', color='#FF0000', user=test_user),
            Category(name='Home', color='#00FF00', user=test_user),
            Category(name='Hobby', color='#0000FF', user=test_user)
        ]
        for category in categories:
            db.session.add(category)
        db.session.commit()

        # Create test tasks
        tasks = [
            Task(
                title='Task 1',
                description='Task 1 description',
                due_date=datetime.now() + timedelta(days=1),
                priority='high',
                category=categories[0],
                user=test_user
            ),
            Task(
                title='Task 2',
                description='Task 2 description',
                due_date=datetime.now() + timedelta(days=2),
                priority='medium',
                category=categories[1],
                user=test_user
            ),
            Task(
                title='Task 3',
                description='Task 3 description',
                due_date=datetime.now() + timedelta(days=3),
                priority='low',
                category=categories[2],
                user=test_user
            )
        ]
        for task in tasks:
            db.session.add(task)
        db.session.commit()

        print("Test data has been added to the database.")

if __name__ == '__main__':
    test_database() 