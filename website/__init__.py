import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = os.environ.get("DATABASE_URL")
login_manager = LoginManager()


def create_app():
    from .views import views
    from .auth import auth
    from .models import User, Note

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    # create_database(app)

    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')
