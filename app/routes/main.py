from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.auth_forms import LoginForm, RegisterForm
from app.models.models import User, db
from flask_login import login_user

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    login_form = LoginForm(prefix="login")
    register_form = RegisterForm(prefix="register")

    if login_form.validate_on_submit() and login_form.submit.data:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("tasks.get_tasks"))
        else:
            flash("Invalid login credentials.", "danger")

    if register_form.validate_on_submit() and register_form.submit.data:
        existing_user = User.query.filter_by(email=register_form.email.data).first()
        if existing_user:
            flash("Email already registered.", "danger")
        else:
            user = User(username=register_form.username.data, email=register_form.email.data)
            user.set_password(register_form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("main.index"))

    return render_template("index.html", login_form=login_form, register_form=register_form)
