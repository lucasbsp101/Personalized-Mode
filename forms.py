from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length

class PersonalDataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    hobbies = TextAreaField('Hobbies')
    work = TextAreaField('Work')
    submit = SubmitField('Submit')