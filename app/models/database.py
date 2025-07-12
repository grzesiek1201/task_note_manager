"""
app/models/database.py

Initializes the database for the project.

Only use for development or testing purposes.
"""

from flask import Flask
from app.extensions import db
from app.models.models import User  # fixed import to absolute path


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
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres.uzktibwarkomgvnlmswf:plemiona1201@aws-0-eu-central-1.pooler.supabase.com:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    if config_object:
        if isinstance(config_object, str):
            app.config.from_object(config_object)
        elif isinstance(config_object, dict):
            app.config.update(config_object)
        else:
            raise TypeError("config_object must be a str or dict")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    print("✅ Tables created.")
