from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='This field is required.'), Length(min=1, max=50)])
    color = StringField('Color', default='#000000')
    submit = SubmitField('Save')
