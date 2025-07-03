from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from task_note_manager.app import db
from task_note_manager.app.auth import auth_bp
from task_note_manager.app.auth.forms import LoginForm, RegisterForm
from task_note_manager.app.models.models import User
from task_note_manager.app.init_data import init_default_categories


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return render_template('auth/login.html', title='Login', form=form)
        login_user(user, remember=form.remember.data)
        flash('Welcome!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if not form.password.data or len(form.password.data) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('auth/register.html', title='Registration', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        init_default_categories(user.id)
        flash('Congratulations, registration was successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Registration', form=form) 