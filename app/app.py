from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # wyłącza nadmiarowe śledzenie zmian

db.init_app(app)

with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele w bazie danych
