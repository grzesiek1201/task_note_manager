from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User, Task, Note, Category


class LoginForm(FlaskForm):
    """
    Login form.
    
    Attributes:
        username: Username field.
        password: Password field.
        remember_me: Remember me field.
        submit: Submit button.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """
    Registration form.
    
    Attributes:
        username: Username field.
        email: Email field.
        password: Password field.
        password2: Confirm password field.
        submit: Submit button.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Checks if the username is unique.
        
        Args:
            username: Username to check.
        
        Raises:
            ValidationError: If the username already exists.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Checks if the email is unique.
        
        Args:
            email: Email to check.
        
        Raises:
            ValidationError: If the email already exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TaskForm(FlaskForm):
    """
    Task form.
    
    Attributes:
        title: Title field.
        description: Description field.
        due_date: Due date field.
        priority: Priority field.
        category_id: Category field.
        submit: Submit button.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeField('Due date', format='%Y-%m-%d %H:%M')
    priority = SelectField('Priority', choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Save')


class NoteForm(FlaskForm):
    """
    Note form.
    
    Attributes:
        title: Title field.
        content: Content field.
        category_id: Category field.
        submit: Submit button.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Save')


class CategoryForm(FlaskForm):
    """
    Category form.
    
    Attributes:
        name: Name field.
        color: Color field.
        submit: Submit button.
    """
    name = StringField('Name', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    submit = SubmitField('Save')
