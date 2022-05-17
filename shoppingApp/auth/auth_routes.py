from flask import Blueprint, render_template, url_for, redirect, flash
from shoppingApp.main.forms import SearchForm
from shoppingApp.auth.forms import RegistrationForm, LoginForm
from shoppingApp.operate_user_data import check_user
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from datetime import timedelta

from shoppingApp import db
from shoppingApp.models import User

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@auth.route('/registration', methods=['GET', 'POST'])
def sing_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not check_user(form.email.data):
            new_user = User(first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            email=form.email.data,
                            password=generate_password_hash(form.password.data, method='sha256'),
                            age=form.age.data)
            db.session.add(new_user)
            db.session.commit()

            flash("User created successfully", 'success')
            return redirect(url_for('auth.login'))
        else:
            flash("User with this email already exists, try again", 'danger')
    return render_template('registration.html', title='Sing Up', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:  # Check if the user is not already logged in
        return redirect(url_for('home.index'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = check_user(email)

        if user:
            if check_password_hash(user.password, password):
                print(remember)  # don`t forget to delete!!!
                flask_login.login_user(user, remember=remember, duration=timedelta(days=2))  # check if the 'remember' me is working and is user 'is active'!!!
                print(user.is_active, user.is_anonymous, user.is_authenticated)
                flash(f"{email} logged in successfully", 'success')
                return redirect(url_for('home.index'))
            else:
                flash("Password incorrect, please try again", 'danger')
        else:
            flash("Email incorrect or not exists, please try again", 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home.index'))
