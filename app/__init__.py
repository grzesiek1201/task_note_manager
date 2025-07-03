from flask import Flask
from config import Config
from task_note_manager.app.extensions import db, migrate
from task_note_manager.app.models.models import login

login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from task_note_manager.app.main import main_bp
    from task_note_manager.app.auth import auth_bp
    from task_note_manager.app.tasks import tasks_bp
    from task_note_manager.app.notes import notes_bp
    from task_note_manager.app.categories import categories_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(categories_bp)

    # Wymuszam import modeli, aby były widoczne dla SQLAlchemy
    from task_note_manager.app import models

    return app
