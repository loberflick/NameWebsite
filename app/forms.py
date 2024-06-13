from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models


class Add_Pizza(FlaskForm):
    name = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description')
    base = SelectField('base')
    toppings = SelectMultipleField('toppings')

class Select_Pizza(FlaskForm):
    moviename = SelectField('name', validators=[DataRequired()], coerce=int)

