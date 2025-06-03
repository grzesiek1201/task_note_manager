"""
app/routes/auth.py
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.auth_forms import LoginForm, RegisterForm
from app.models.models import User, db
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            or_(User.email == form.email.data, User.username == form.username.data)
        ).first()
        if existing_user:
            flash("Email or username already registered.", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Database error. Please try again.", "danger")
            return redirect(url_for("auth.register"))
        flash("Account created! You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("tasks.dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
