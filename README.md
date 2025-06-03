# Task Note Manager

## Project Overview

Task Note Manager is a modular Flask web application for managing tasks, notes, and categories with user authentication.  
The app uses SQLAlchemy for ORM, Flask-Migrate for database migrations, and Flask-Login for user session management.

## Features

- User registration and login (Flask-Login)  
- CRUD operations for tasks, notes, and categories  
- Database migrations handled by Flask-Migrate  
- Modular architecture using Blueprints  
- Configurable via environment-specific config classes  
- Unit and integration tests with pytest  

## Technology Stack

- Python 3.12  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-Login  
- PostgreSQL (production/test DB)  
- pytest for testing  

## Project Structure

app/
├── init.py # app factory, extensions initialization, blueprint registration
├── models/
│ └── models.py # SQLAlchemy models (User, Task, Note, Category)
├── routes/
│ ├── auth.py # authentication routes
│ ├── tasks.py # task management routes
│ ├── notes.py # notes management routes
│ └── categories.py # categories management routes
├── templates/ # Jinja2 HTML templates
└── static/ # static files (CSS, JS, images)
tests/
├── test_auth.py
├── test_tasks.py
└── ...
config.py # configuration classes (DevelopmentConfig, TestingConfig, ProductionConfig)
requirements.txt # dependencies


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/grzesiek1201/task_note_manager.git
   cd task_note_manager
(Optional) Create and activate a Python virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install dependencies:

pip install -r requirements.txt
Set up PostgreSQL database and update connection URI in config.py.

Initialize the database and run migrations:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Run the application:

flask run
Running Tests
Run all tests with pytest:

pytest tests/
Configuration
Configurations are handled in config.py. By default, the app uses the DevelopmentConfig.
Override environment variables or modify the config file to adjust settings (database URI, debug mode, etc.).

License
- MIT License
