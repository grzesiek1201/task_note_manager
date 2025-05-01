"""
__init__.py
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import models

    from .routes import auth, tasks, notes, categories
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(categories.bp)

    return app
