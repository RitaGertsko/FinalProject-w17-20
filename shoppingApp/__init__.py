from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shoppingApp.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from shoppingApp import auth, main

    # blueprint for main routes in our app
    from shoppingApp.main.main_routes import home as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix="/home")

    # blueprint for auth routes in our app
    from shoppingApp.auth.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from shoppingApp import config, models, operate_user_data

    return app
