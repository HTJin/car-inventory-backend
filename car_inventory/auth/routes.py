from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import LoginForm
from ..models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_template')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            user = User(email, password=password)
            db.session.add(user)
            db.session.commit()
            
            print('User created, redirecting to Login')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid Form Data')
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                print('Authenticated')
                login_user(logged_user)
                return redirect(url_for('site.home'))
            else:
                print('Incorrect password')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid Form Data')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print('You are logged out')
    return redirect(url_for('site.home'))