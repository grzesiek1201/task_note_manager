from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Provide shell context for Flask CLI.
    
    Returns:
        dict: Dictionary containing database and model objects for shell access.
    """
    from app.models.models import User, Task, Note, Category
    return {'db': db, 'User': User, 'Task': Task, 'Note': Note, 'Category': Category}


if __name__ == '__main__':
    app.run(debug=True)
