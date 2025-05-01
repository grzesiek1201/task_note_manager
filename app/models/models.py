"""
models.py

Defines the SQLAlchemy ORM models for the User, Task, Note, and Category tables,
including password hashing, task management, and note handling.

Classes:
    - User: Represents a user in the system and provides methods for password hashing and checking.
    - Category: Represents a category for grouping tasks and notes.
    - Note: Represents a note that belongs to a user and is optionally categorized.
    - Task: Represents a task associated with a user and a category.

Relationships:
    - A User can have multiple Notes, Tasks, and Categories.
    - Notes and Tasks can belong to a specific Category.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    """
    ORM model representing a user in the system.

    Attributes:
        id (int): Primary key, unique user ID.
        username (str): Unique username for login purposes.
        password (str): Hashed password (never stored in plain text).
        email (str): Unique email address of the user.
        notes (str) : Notes from the user.
        tasks (str) : Tasks from the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)
    tasks = db.relationship("Task", backref="user", lazy=True)
    categories = db.relationship("Category", backref="user", lazy=True)

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


class Category(db.Model):
    """
    ORM model representing a category for tasks and notes.

    Attributes:
        id (int): Primary key, unique category ID.
        name (str): The name of the category.
        user_id (int): Foreign key that links the category to a specific user.

    Relationships:
        - A Category can have many Notes and Tasks.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes = db.relationship("Note", backref="category_obj", lazy=True)
    tasks = db.relationship("Task", backref="category_obj", lazy=True)


class Note(db.Model):
    """
    ORM model representing a note associated with a user and an optional category.

    Attributes:
        id (int): Primary key, unique note ID.
        title (str): Title of the note.
        content (str): Content of the note.
        category_id (int): Foreign key that links the note to a category.
        created_at (datetime): Timestamp when the note was created.
        updated_at (datetime): Timestamp when the note was last updated.
        user_id (int): Foreign key that links the note to a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Task(db.Model):
    """
    ORM model representing a task associated with a user and an optional category.

    Attributes:
        id (int): Primary key, unique task ID.
        title (str): Title of the task.
        description (str): Description of the task.
        due_date (datetime): Due date for the task.
        category_id (int): Foreign key that links the task to a category.
        completed (bool): Flag indicating whether the task has been completed.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
        user_id (int): Foreign key that links the task to a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
