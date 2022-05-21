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
    migrate.init_app(app, db)

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

    # blueprint for auth routes in our app
    from shoppingApp.auth.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # blueprint for profile routes in our app
    from shoppingApp.profile.profile_routes import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix="/profile")

    from shoppingApp import config, operate_user_data, models

    return app
