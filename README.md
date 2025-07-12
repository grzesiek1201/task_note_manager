# Task Note Manager

A web application for managing tasks and notes with categories, priorities, and user authentication.

## 🔗 Live Demo

👉 **Try the app now:**  
[https://task-note-manager.onrender.com](https://task-note-manager.onrender.com/login?next=%2F)

This app is deployed on **Render** and uses **Supabase PostgreSQL** as the production database.

## Features
- User authentication and registration
- Task management (create, edit, delete, set priority, set deadline, assign category)
- Note management (create, edit, delete, assign category)
- Category management (create, edit, delete, assign color)
- Dashboard with statistics
- Responsive user interface (Bootstrap 5)
- Database migrations
- Unit tests

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/grzesiek1201/task_note_manager.git
   cd task_note_manager
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and adjust settings if needed.

5. **Initialize the database:**
   ```sh
   flask db upgrade
   ```

6. **Run the application:**
   ```sh
   flask run
   ```

## Running tests

```sh
pytest --cov=app --cov-report=term-missing
```

## Deployment
This application is deployed on Render with the backend connected to a Supabase PostgreSQL database.
Render handles automatic deployments from GitHub.
Database connection is configured via the DATABASE_URL environment variable.
All secrets and credentials should be set via Render’s environment settings panel.

## Demo

[![Watch the demo](https://img.youtube.com/vi/5y79kmB27M/0.jpg)](https://www.youtube.com/watch?v=_5y79kmB27M)


## License
MIT
