"""
models.py

Defines the SQLAlchemy ORM model for the User table, including password hashing
and verification logic using Werkzeug.

Classes:
    - User: Stores user credentials and provides password utility methods.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """
    ORM model representing a user in the system.

    Attributes:
        id (int): Primary key, unique user ID.
        username (str): Unique username for login purposes.
        password (str): Hashed password (never stored in plain text).
        email (str): Unique email address of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        """
        Hashes and sets the user's password.

        Args:
            password (str): Plain-text password provided by the user.

        Note:
            This method uses Werkzeug's `generate_password_hash` to securely hash passwords
            before storing them in the database.
        """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifies that a plain-text password matches the hashed password.

        Args:
            password (str): Plain-text password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.

        Note:
            Uses Werkzeug's `check_password_hash` for secure verification.
        """
        return check_password_hash(self.password, password)
