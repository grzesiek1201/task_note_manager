from app.models import Category, db
from flask_login import current_user


def init_default_categories(user_id):
    """Inicjalizuje domyślne kategorie dla nowego użytkownika."""
    default_categories = [
        'Praca',
        'Dom',
        'Zakupy',
        'Zdrowie',
        'Rozrywka',
        'Inne'
    ]
    
    for category_name in default_categories:
        category = Category(name=category_name, user_id=user_id)
        db.session.add(category)
    
    db.session.commit()
