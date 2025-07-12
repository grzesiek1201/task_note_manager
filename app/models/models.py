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
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    notes = db.relationship(
        "Note", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    tasks = db.relationship(
        "Task", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    categories = db.relationship(
        "Category", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Hash and set user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def as_dict(self) -> dict:
        """Return user data as dict (excluding sensitive fields)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Category(db.Model):
    __tablename__ = "category"
    __table_args__ = (
        db.UniqueConstraint("name", "user_id", name="_user_category_uc"),
        db.Index("idx_category_user", "user_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    notes = db.relationship(
        "Note", backref="category_obj", lazy="dynamic", cascade="all, delete-orphan"
    )
    tasks = db.relationship(
        "Task", backref="category_obj", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.name}>"

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }


class Note(db.Model):
    __tablename__ = "note"
    __table_args__ = (
        db.Index("idx_note_user", "user_id"),
        db.Index("idx_note_category", "category_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    category = db.relationship("Category", overlaps="category_obj,notes")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.title}>"

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = (
        db.Index("idx_task_user", "user_id"),
        db.Index("idx_task_category", "category_id"),
        db.Index("idx_task_completed", "completed"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", overlaps="category_obj,tasks")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    priority = db.Column(db.String(20), default='medium')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def mark_done(self) -> None:
        """Mark the task as completed. Remember to commit the session manually."""
        self.completed = True
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        status = "[done]" if self.completed else ""
        return f"<Task {self.title} {status}>"

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
