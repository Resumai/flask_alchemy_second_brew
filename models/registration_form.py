from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from models.password_validator import CustomPasswordValidator


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired(), Email(message='Invalid email address.')])
    password = PasswordField(
        'Password:', 
        validators=[DataRequired(), 
        Length(min=8, max=20), 
        CustomPasswordValidator()]
    )

    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), 
            EqualTo('password', 
            message='Passwords must match'
            )
        ]
    )
    submit = SubmitField('Register')