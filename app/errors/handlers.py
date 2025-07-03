from flask import render_template
from task_note_manager.app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Obsługuje błąd 404 (Nie znaleziono).
    
    Args:
        error: Obiekt błędu.
    
    Returns:
        render_template: Szablon strony błędu 404.
    """
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Obsługuje błąd 500 (Wewnętrzny błąd serwera).
    
    Args:
        error: Obiekt błędu.
    
    Returns:
        render_template: Szablon strony błędu 500.
    """
    return render_template('errors/500.html'), 500
