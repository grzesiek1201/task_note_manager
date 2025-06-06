from flask import render_template
from flask_login import login_required, current_user
from app.models import Task, Note, Category
from app.main import main_bp


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    """
    Wyświetla stronę główną z listą zadań, notatek i kategorii użytkownika.
    
    Returns:
        render_template: Szablon strony głównej.
    """
    recent_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).limit(5).all()
    recent_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).limit(5).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    # Statystyki
    task_stats = {
        'total': Task.query.filter_by(user_id=current_user.id).count(),
        'completed': Task.query.filter_by(user_id=current_user.id, completed=True).count(),
        'high_priority': Task.query.filter_by(user_id=current_user.id, priority='high').count(),
        'medium_priority': Task.query.filter_by(user_id=current_user.id, priority='medium').count(),
        'low_priority': Task.query.filter_by(user_id=current_user.id, priority='low').count()
    }
    
    note_stats = {
        'total': Note.query.filter_by(user_id=current_user.id).count(),
        'with_category': Note.query.filter_by(user_id=current_user.id).filter(Note.category_id.isnot(None)).count(),
        'without_category': Note.query.filter_by(user_id=current_user.id).filter(Note.category_id.is_(None)).count()
    }
    
    return render_template('index.html', title='Strona główna',
                         recent_tasks=recent_tasks,
                         recent_notes=recent_notes,
                         categories=categories,
                         task_stats=task_stats,
                         note_stats=note_stats)
