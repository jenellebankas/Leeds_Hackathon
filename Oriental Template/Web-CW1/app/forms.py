from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class AssessmentForm(FlaskForm):
    assessment_title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    module_code = StringField('Module Code', validators=[DataRequired(), Length(max=10)])
    deadline_date = DateTimeField('Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=200)])
    status = BooleanField('Completed')
    submit = SubmitField('Save')