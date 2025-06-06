from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired(), Length(min=1, max=50)])
    color = StringField('Kolor', default='#000000')
    submit = SubmitField('Zapisz')
