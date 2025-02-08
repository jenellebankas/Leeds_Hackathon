from flask_wtf import FlaskForm
from wtforms import DateField,StringField, PasswordField, SubmitField, SelectMultipleField, TextAreaField, DateTimeField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Length


class TaskForm(FlaskForm):
    task_title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    deadline_date = DateTimeField('Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    task_description = TextAreaField('Description', validators=[Length(max=200)])
    task_status = BooleanField('Completed')
    task_progress = IntegerField('Progress')
    submit = SubmitField('Save')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DeleteForm(FlaskForm):
    pass