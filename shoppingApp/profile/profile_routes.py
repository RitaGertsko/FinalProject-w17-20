from flask import Blueprint, render_template, url_for, redirect, flash
from shoppingApp.main.forms import SearchForm
from shoppingApp.profile.forms import ProfileForm
from werkzeug.security import generate_password_hash
import flask_login
from shoppingApp.models import User

from shoppingApp import db

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static')


@profile.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@profile.route('/profile-info', methods=['GET', 'POST'])
@flask_login.login_required
def profile_info():
    current_user = User.query.get(flask_login.current_user.id)

    form = ProfileForm()

    if form.validate_on_submit():
        if form.first_name.data == "" or form.first_name.data is None:
            current_user.first_name = current_user.first_name
        else:
            current_user.first_name = str(form.first_name.data).capitalize()

        if form.last_name.data == "" or form.last_name.data is None:
            current_user.last_name = current_user.last_name
        else:
            current_user.last_name = str(form.last_name.data).capitalize()

        if form.password.data == "" or form.first_name.data is None:
            current_user.password = current_user.password
        else:
            current_user.password = str(generate_password_hash(form.password.data, method='sha256'))

        if current_user is None:
            current_user.age = 'No recorde of '
        elif form.age.data is None:
            current_user.age = current_user.age
        else:
            current_user.age = str(form.age.data)

        db.session.commit()

        flash("Changes saved successfully", 'success')
        return redirect(url_for('profile.profile_info'))

    return render_template('profile.html', title='Profile', form=form, user=current_user)
