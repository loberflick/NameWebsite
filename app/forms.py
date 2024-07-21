from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models


class Add_Account(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class Add_Class(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('name', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired()])


class Add_Student(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    picture = FileField('name', validators=[DataRequired()])
    student_id = IntegerField('name', validators=[DataRequired()])

