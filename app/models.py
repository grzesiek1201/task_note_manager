from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    """
    Model użytkownika.
    
    Attributes:
        id: ID użytkownika.
        username: Nazwa użytkownika.
        email: Adres email użytkownika.
        password_hash: Zaszyfrowane hasło użytkownika.
        tasks: Lista zadań użytkownika.
        notes: Lista notatek użytkownika.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacje
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    notes = db.relationship('Note', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')

    def set_password(self, password):
        """
        Ustawia hasło użytkownika.
        
        Args:
            password: Hasło do ustawienia.
        """
        print(f"[DIAG] Ustawianie hasła: {password}")
        self.password_hash = generate_password_hash(password)
        print(f"[DIAG] Wygenerowany hash: {self.password_hash}")

    def check_password(self, password):
        """
        Sprawdza, czy podane hasło jest poprawne.
        
        Args:
            password: Hasło do sprawdzenia.
        
        Returns:
            bool: True, jeśli hasło jest poprawne, w przeciwnym razie False.
        """
        print(f"[DIAG] Sprawdzanie hasła: {password}")
        print(f"[DIAG] Przeciwko hash: {self.password_hash}")
        result = check_password_hash(self.password_hash, password)
        print(f"[DIAG] Wynik sprawdzenia: {result}")
        return result

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    """
    Model zadania.
    
    Attributes:
        id: ID zadania.
        title: Tytuł zadania.
        description: Opis zadania.
        due_date: Termin wykonania zadania.
        priority: Priorytet zadania.
        completed: Czy zadanie jest wykonane.
        created_at: Data utworzenia zadania.
        user_id: ID użytkownika, który utworzył zadanie.
        category_id: ID kategorii zadania.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    priority = db.Column(db.String(20), default='medium')

    category = db.relationship('Category', backref=db.backref('tasks', lazy='dynamic'))

    def __repr__(self):
        return f'<Task {self.title}>'


class Note(db.Model):
    """
    Model notatki.
    
    Attributes:
        id: ID notatki.
        title: Tytuł notatki.
        content: Treść notatki.
        created_at: Data utworzenia notatki.
        user_id: ID użytkownika, który utworzył notatkę.
        category_id: ID kategorii notatki.
    """
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship('Category', backref=db.backref('notes', lazy='dynamic'))

    def __repr__(self):
        return f'<Note {self.title}>'


class Category(db.Model):
    """
    Model kategorii.
    
    Attributes:
        id: ID kategorii.
        name: Nazwa kategorii.
        color: Kolor kategorii.
        tasks: Lista zadań w kategorii.
        notes: Lista notatek w kategorii.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
