from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shoppingApp.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from shoppingApp.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from shoppingApp import auth, main

    # blueprint for main routes in our app
    from shoppingApp.main.main_routes import home as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix="/home")
    app.register_blueprint(home_blueprint, url_prefix="/")

    # blueprint for auth routes in our app
    from shoppingApp.auth.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # blueprint for profile routes in our app
    from shoppingApp.profile.profile_routes import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix="/profile")

    # blueprint for products routes in our app
    from shoppingApp.products.products_routes import product as product_blueprint
    app.register_blueprint(product_blueprint, url_prefix="/product")

    # blueprint for cart routes in our app
    from shoppingApp.cart.cart_routes import cart as cart_blueprint
    app.register_blueprint(cart_blueprint, url_prefix="/cart")

    # blueprint for errors routes in our app
    from shoppingApp.errors.errors_routes import errors as error_blueprint
    app.register_blueprint(error_blueprint, url_prefix="/error")

    from shoppingApp import config, operate_user_data, models

    return app
