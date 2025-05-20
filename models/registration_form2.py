from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegistrationStep2Form(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    surname = StringField('Surname:', validators=[DataRequired()])
    address = StringField('Address:', validators=[DataRequired()])
    submit = SubmitField('Submit')