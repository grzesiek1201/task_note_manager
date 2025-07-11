from app.models.models import Category
from app import db
from flask_login import current_user


def init_default_categories(user_id):
    """Inicjalizuje domyślne kategorie dla nowego użytkownika."""
    default_categories = [
        'Work',
        'Home',
        'Shopping',
        'Health',
        'Entertainment',
        'Other'
    ]
    
    for category_name in default_categories:
        category = Category(name=category_name, user_id=user_id)
        db.session.add(category)
    
    db.session.commit()
