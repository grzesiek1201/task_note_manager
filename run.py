from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models.models import User, Task, Note, Category
    return {'db': db, 'User': User, 'Task': Task, 'Note': Note, 'Category': Category}


if __name__ == '__main__':
    app.run(debug=True)
