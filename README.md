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


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/grzesiek1201/task_note_manager.git
   cd task_note_manager

License
- MIT License
