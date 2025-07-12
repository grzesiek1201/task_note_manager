from flask import Flask
from config import Config
from .extensions import db, migrate, login


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from .main import main_bp
    from .auth import auth_bp
    from .tasks import tasks_bp
    from .notes import notes_bp
    from .categories import categories_bp
    from .errors import bp as errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(errors_bp)

    # Wymuszam import modeli, aby były widoczne dla SQLAlchemy
    from . import models

    return app
