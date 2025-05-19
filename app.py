from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length
from sqlalchemy import select, or_
from string import punctuation as valid_symbols
from db import db
from models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
with app.app_context():
    db.create_all()



class CustomPasswordValidator():
    def __init__(self):
        self.message = 'Password must have at least one upper letter, one lower letter, one symbol, one number and no space.'

    def __call__(self, form, field):
        text : str = field.data
        is_any_upper = any(c.isupper() for c in text)
        is_any_lower = any(c.islower() for c in text)
        is_any_number = any(c.isdigit() for c in text)
        is_no_space = not any(c.isspace() for c in text)
        is_any_symbol = any(c in valid_symbols for c in text)
        if not all([is_any_upper, is_any_lower, is_any_number, is_no_space, is_any_symbol]):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=20), CustomPasswordValidator()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return 'User registered successfully'
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        selection = select(User).where(or_(
            User.username == form.username_or_email.data,
            User.email == form.username_or_email.data
            )
        )
        user = db.session.execute(selection).scalar_one_or_none()

        if not user:
            return 'No account found with that username or email'

        if user.password == form.password.data:
            return 'User logged in successfully'
        return 'Invalid login credentials or password'
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
