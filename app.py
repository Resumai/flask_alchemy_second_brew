from flask import Flask, render_template, redirect, url_for, session, flash
from sqlalchemy import select, or_
from db import db
from models import User, UserDetails, RegistrationForm, RegistrationStep2Form, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=password_hash
        )
        db.session.add(user)
        db.session.commit()
        session['current_user_id'] = user.id
        # return 'User registered successfully'
        return redirect(url_for('register_step2'))
    return render_template('register.html', form=form)


@app.route('/register/step2', methods=['GET', 'POST'])
def register_step2():
    form = RegistrationStep2Form()
    
    current_user_id = session.get('current_user_id')
    if not current_user_id:
        return redirect(url_for('register'))
    
    if form.validate_on_submit():
        
        user_details = UserDetails(
            user_id=current_user_id, 
            name=form.name.data, 
            surname=form.surname.data, 
            address=form.address.data
        )
        db.session.add(user_details)
        db.session.commit()

        session.pop('current_user_id', None)

        return redirect(url_for('login'))
    return render_template('register_step2.html', form=form)


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
            flash('No account found with that username or email', 'error')
            return redirect(url_for('login'))
        
        if check_password_hash(user.password, form.password.data):
            # session['current_user_id'] = user.id
            flash('User logged in successfully', 'success')
            return redirect(url_for('login'))
        flash('Invalid login credentials or password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
