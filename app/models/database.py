"""
app/models/database.py

Initializes the database for the project.

Only use for development or testing purposes.
"""

from flask import Flask
from app.extensions import db
from app.models import models


def create_app(config_object=None) -> Flask:
    """
    Creates a minimal Flask app instance and initializes the database.

    Args:
        config_object (Optional): Optional configuration object or dict.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/Users",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    if config_object:
        app.config.from_object(config_object) if isinstance(config_object, str) else app.config.update(config_object)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    print("✅ Tables created.")
