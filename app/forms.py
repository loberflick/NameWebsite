from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SelectMultipleField, FileField, RadioField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models


class Add_Account(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class Add_Class(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('name', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired()])


class Add_Student(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired()])
    student_id = IntegerField('student id', validators=[DataRequired()])


class Quiz(FlaskForm):
    guess = RadioField('guess', validators=[DataRequired()])
