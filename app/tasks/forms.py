from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='This field is required.'), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    due_date = DateTimeField('Due date', format='%Y-%m-%dT%H:%M', validators=[Optional()], default=datetime.now)
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[DataRequired(message='This field is required.')])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired(message='This field is required.')])
    submit = SubmitField('Save')
