"""
Flask extensions and configuration.

This module contains Flask extensions initialization and configuration
for SQLAlchemy, Flask-Login, and Flask-Migrate.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import timedelta

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

# Konfiguracja login managera
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
login.login_message_category = "info"
login.session_protection = "strong"

# Konfiguracja sesji
PERMANENT_SESSION_LIFETIME = timedelta(days=1)

@login.user_loader
def load_user(id):
    """Load user by ID for Flask-Login.
    
    Args:
        id: The user ID to load.
        
    Returns:
        User: The user object if found, None otherwise.
    """
    from app.models.models import User
    return User.query.get(int(id))
