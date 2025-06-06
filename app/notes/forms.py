from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Treść', validators=[DataRequired(), Length(min=1, max=1000)])
    category_id = SelectField('Kategoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Zapisz')
