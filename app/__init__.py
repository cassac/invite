from flask import Flask
import sqlite3
import os
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from config import email_config, config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ## CONFIG PLACED BEFORE FLASK-MAIL INSTANCE
    app.config.update(dict(
        MAIL_DEBUG = email_config['MAIL_DEBUG'],
        MAIL_SERVER = email_config['MAIL_SERVER'],
        MAIL_PORT= email_config['MAIL_PORT'],
        MAIL_USE_SSL= email_config['MAIL_USE_SSL'],
        MAIL_USERNAME = email_config['MAIL_USERNAME'],
        MAIL_PASSWORD = email_config['MAIL_PASSWORD'],
        MAIL_SUPPRESS_SEND = email_config['MAIL_SUPPRESS_SEND'],
        TESTING = email_config['TESTING']
    ))
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
