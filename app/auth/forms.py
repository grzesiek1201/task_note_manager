from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.models import User


class RegisterForm(FlaskForm):
    """Registration form for new users.
    
    Attributes:
        username: Username field with length validation.
        email: Email field with email format validation.
        password: Password field with minimum length validation.
        password2: Password confirmation field.
        submit: Submit button.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Validate that the username is unique.
        
        Args:
            username: Username field to validate.
            
        Raises:
            ValidationError: If the username already exists.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate that the email is unique.
        
        Args:
            email: Email field to validate.
            
        Raises:
            ValidationError: If the email already exists.
        """
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    """Login form for existing users.
    
    Attributes:
        username: Username field.
        password: Password field.
        remember: Remember me checkbox.
        submit: Submit button.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
