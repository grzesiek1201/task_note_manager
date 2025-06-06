from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """
    Formularz logowania.
    
    Attributes:
        username: Pole nazwy użytkownika.
        password: Pole hasła.
        remember_me: Pole zapamiętania użytkownika.
        submit: Przycisk zatwierdzający.
    """
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class RegistrationForm(FlaskForm):
    """
    Formularz rejestracji.
    
    Attributes:
        username: Pole nazwy użytkownika.
        email: Pole adresu email.
        password: Pole hasła.
        password2: Pole potwierdzenia hasła.
        submit: Przycisk zatwierdzający.
    """
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        """
        Sprawdza, czy nazwa użytkownika jest unikalna.
        
        Args:
            username: Nazwa użytkownika do sprawdzenia.
        
        Raises:
            ValidationError: Jeśli nazwa użytkownika już istnieje.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Użyj innej nazwy użytkownika.')

    def validate_email(self, email):
        """
        Sprawdza, czy adres email jest unikalny.
        
        Args:
            email: Adres email do sprawdzenia.
        
        Raises:
            ValidationError: Jeśli adres email już istnieje.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Użyj innego adresu email.')


class TaskForm(FlaskForm):
    """
    Formularz zadania.
    
    Attributes:
        title: Pole tytułu zadania.
        description: Pole opisu zadania.
        due_date: Pole terminu wykonania zadania.
        priority: Pole priorytetu zadania.
        category: Pole kategorii zadania.
        submit: Przycisk zatwierdzający.
    """
    title = StringField('Tytuł', validators=[DataRequired()])
    description = TextAreaField('Opis')
    due_date = DateTimeField('Termin', format='%Y-%m-%d %H:%M')
    priority = SelectField('Priorytet', choices=[('high', 'Wysoki'), ('normal', 'Normalny'), ('low', 'Niski')])
    category = SelectField('Kategoria', coerce=int)
    submit = SubmitField('Zapisz')


class NoteForm(FlaskForm):
    """
    Formularz notatki.
    
    Attributes:
        title: Pole tytułu notatki.
        content: Pole treści notatki.
        category: Pole kategorii notatki.
        submit: Przycisk zatwierdzający.
    """
    title = StringField('Tytuł', validators=[DataRequired()])
    content = TextAreaField('Treść')
    category = SelectField('Kategoria', coerce=int)
    submit = SubmitField('Zapisz')


class CategoryForm(FlaskForm):
    """
    Formularz kategorii.
    
    Attributes:
        name: Pole nazwy kategorii.
        color: Pole koloru kategorii.
        submit: Przycisk zatwierdzający.
    """
    name = StringField('Nazwa', validators=[DataRequired()])
    color = StringField('Kolor', validators=[DataRequired()])
    submit = SubmitField('Zapisz')
