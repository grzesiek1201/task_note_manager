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

```text
app/
├── __init__.py
├── models/
│   └── models.py
├── routes/
│   ├── auth.py
│   ├── tasks.py
│   ├── notes.py
│   └── categories.py
templates/
static/
config.py
requirements.txt
README.md



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/grzesiek1201/task_note_manager.git
   cd task_note_manager

License
- MIT License
