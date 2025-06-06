"""
Skrypt do testowania połączenia z bazą danych.
"""

from app import create_app, db
from app.models import User, Task, Category
from datetime import datetime, timedelta

def test_database():
    app = create_app()
    with app.app_context():
        # Tworzenie użytkownika testowego
        test_user = User(username='test_user', email='test@example.com')
        test_user.set_password('test_password')
        db.session.add(test_user)
        db.session.commit()

        # Tworzenie kategorii testowych
        categories = [
            Category(name='Praca', color='#FF0000', user=test_user),
            Category(name='Dom', color='#00FF00', user=test_user),
            Category(name='Hobby', color='#0000FF', user=test_user)
        ]
        for category in categories:
            db.session.add(category)
        db.session.commit()

        # Tworzenie zadań testowych
        tasks = [
            Task(
                title='Zadanie 1',
                description='Opis zadania 1',
                due_date=datetime.now() + timedelta(days=1),
                priority='high',
                category=categories[0],
                user=test_user
            ),
            Task(
                title='Zadanie 2',
                description='Opis zadania 2',
                due_date=datetime.now() + timedelta(days=2),
                priority='medium',
                category=categories[1],
                user=test_user
            ),
            Task(
                title='Zadanie 3',
                description='Opis zadania 3',
                due_date=datetime.now() + timedelta(days=3),
                priority='low',
                category=categories[2],
                user=test_user
            )
        ]
        for task in tasks:
            db.session.add(task)
        db.session.commit()

        print("Dane testowe zostały dodane do bazy danych.")

if __name__ == '__main__':
    test_database() 