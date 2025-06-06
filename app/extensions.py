"""
app/extensions.py
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Konfiguracja login managera
login_manager.login_view = "auth.login"
login_manager.login_message = "Proszę się zalogować, aby uzyskać dostęp do tej strony."
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

# Konfiguracja sesji
PERMANENT_SESSION_LIFETIME = timedelta(days=1)


@login_manager.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))
