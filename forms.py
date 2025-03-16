from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class PersonalDataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    age = IntegerField('Age', validators=[DataRequired()])
    hobbies = TextAreaField('Hobbies', validators=[Optional()])
    work = TextAreaField('Work', validators=[Optional()])
    submit = SubmitField('Submit')