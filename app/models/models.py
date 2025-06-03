"""
app/models/models.py

Defines the SQLAlchemy ORM models for the User, Task, Note, and Category tables.

Classes:
    - User: Represents a user in the system. Handles password hashing and verification.
    - Category: Represents a category for grouping tasks and notes.
    - Note: Represents a note associated with a user and optionally a category.
    - Task: Represents a task associated with a user and optionally a category.

Relationships:
    - A User can have many Notes, Tasks, and Categories.
    - A Category can have many Notes and Tasks.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Represents an authenticated user of the system."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    notes = db.relationship("Note", backref="user", lazy="dynamic")
    tasks = db.relationship("Task", backref="user", lazy="dynamic")
    categories = db.relationship("Category", backref="user", lazy="dynamic")

    def set_password(self, password: str) -> None:
        """Hash and set user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model):
    """Represents a category that can group tasks and notes."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    notes = db.relationship("Note", backref="category_obj", lazy="dynamic")
    tasks = db.relationship("Task", backref="category_obj", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"


class Note(db.Model):
    """Represents a textual note owned by a user, optionally categorized."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Note {self.title}>"


class Task(db.Model):
    """Represents a task that a user wants to track or complete."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<Task {self.title} {'[done]' if self.completed else ''}>"
