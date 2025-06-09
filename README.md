# Task Note Manager

**Task Note Manager** is a modern web application for managing tasks and notes, built with Python and the Flask framework. It features an intuitive user interface, advanced organization tools, and a flexible category system.

## Features

### ✅ Task Management
- Create, edit, and delete tasks
- Set priority levels (High, Medium, Low)
- Assign due dates
- Categorize tasks
- Mark tasks as completed

### 📝 Note Management
- Create, edit, and delete notes
- Text formatting support
- Categorize notes
- Quick access to recent notes

### 🗂️ Category System
- Create custom categories
- Assign colors to categories
- Filter tasks and notes by category

### 📊 Statistics & Reports
- Task statistics by priority
- Note statistics by category
- Charts and visual data summaries

## Tech Stack

- **Backend:** Python 3.8+, Flask 2.0+, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Database:** PostgreSQL
- **Dev Tools:** Virtualenv, Flask-Migrate, pip, Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/task-note-manager.git
cd task-note-manager
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

3. Install dependencies::
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit the .env file with your settings
```

5. Initialize the database::
```bash
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Project Structure

```
task-note-manager/
├── app/
│   ├── auth/           # Authentication module
│   ├── tasks/          # Task logic
│   ├── notes/          # Notes logic
│   ├── categories/     # Categories logic
│   ├── main/           # Core views
│   ├── models/         # Data models
│   ├── templates/      # HTML templates
│   └── static/         # Static assets (CSS/JS)
├── migrations/         # Database migrations
├── tests/              # Unit tests
├── config.py           # App configuration
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Tests

run:
```bash
python -m pytest
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Grzegorz Żywicki

## Version

1.0.0
