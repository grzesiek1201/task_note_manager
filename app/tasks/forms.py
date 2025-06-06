from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


class TaskForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Opis', validators=[Length(max=500)])
    due_date = DateTimeField('Termin', format='%Y-%m-%dT%H:%M', validators=[Optional()], default=datetime.now)
    priority = SelectField('Priorytet', choices=[
        ('low', 'Niski'),
        ('medium', 'Średni'),
        ('high', 'Wysoki')
    ], validators=[DataRequired()])
    category_id = SelectField('Kategoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Zapisz')
