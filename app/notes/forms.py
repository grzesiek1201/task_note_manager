from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='This field is required.'), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired(message='This field is required.'), Length(min=1, max=1000)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired(message='This field is required.')])
    submit = SubmitField('Save')
