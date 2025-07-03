from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from task_note_manager.app import db
from task_note_manager.app.models.models import Task, Category
from task_note_manager.app.tasks import tasks_bp
from task_note_manager.app.tasks.forms import TaskForm


@tasks_bp.route('/tasks')
@login_required
def tasks():
    """Display the list of user's tasks."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form = TaskForm()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    return render_template('tasks.html', title='Tasks', tasks=tasks, form=form, categories=categories)


@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task."""
    form = TaskForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            category_id=form.category_id.data if form.category_id.data else None,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task has been created!', 'success')
        return redirect(url_for('tasks.tasks'))
    
    return render_template('create_task.html', title='New task', form=form)


@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """Edit an existing task."""
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('tasks.tasks'))
    
    form = TaskForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.category_id = form.category_id.data if form.category_id.data else None
        db.session.commit()
        flash('Task has been updated!', 'success')
        return redirect(url_for('tasks.tasks'))
    
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.due_date.data = task.due_date
        form.priority.data = task.priority
        form.category_id.data = task.category_id
    
    return render_template('edit_task.html', title='Edit task', form=form, task=task)


@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('tasks.tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('tasks.tasks'))


@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_task(id):
    """Toggle the completion status of a task."""
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to change the status of this task.', 'danger')
        return redirect(url_for('tasks.tasks'))
    
    task.completed = not task.completed
    db.session.commit()
    flash('Task status has been updated!', 'success')
    return redirect(url_for('tasks.tasks'))
