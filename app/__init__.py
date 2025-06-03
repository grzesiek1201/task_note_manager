from flask import Flask
from app.extensions import db, login_manager, migrate
from app.models import models
from app.routes import main


def create_app(config_object="config.DevelopmentConfig") -> Flask:
    app = Flask(__name__)
    if isinstance(config_object, str):
        app.config.from_object(config_object)
    else:
        app.config.update(config_object)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import auth, tasks, notes, categories, main
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(categories.bp)

    # Register user_loader
    from app.models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
