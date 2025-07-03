from task_note_manager.app import create_app, db
from task_note_manager.app.models.models import User, Task, Note, Category

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task, 'Note': Note, 'Category': Category}


if __name__ == '__main__':
    app.run(debug=True)
