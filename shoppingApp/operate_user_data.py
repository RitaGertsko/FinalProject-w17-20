from shoppingApp.models import User

def check_user(email):
    return User.query.filter_by(email=f'{email}').first()

def check_password(email, password):
    return password == User.query.filter_by(email=email).first().password