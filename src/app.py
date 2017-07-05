#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
# from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from config import app_config

import os
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
# login_manager = LoginManager()


def create_app(debug=False):
    app = Flask(__name__)
    # app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    # app.template_folder = app.config.get('TEMPLATE_FOLDER', '')
    # app.static_folder = app.config.get('STATIC_FOLDER', '')

    # bootstrap = Bootstrap(app)
    session = Session(app)

    db.init_app(app)

    # login_manager.init_app(app)
    # login_manager.login_message = "You must be logged in to access this page."
    # login_manager.login_view = "auth.login"

    # migrate = Migrate(app, db)

    # Logging
    log_config = app.config.get("LOG", dict())
    handler = RotatingFileHandler(
        log_config.get("FILENAME"),
        maxBytes=log_config.get("MAX_BYTES"),
        backupCount=log_config.get("BACKUP_COUNT"),
    )
    formatter = logging.Formatter(log_config.get("FORMAT"))
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # from app import models

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

    # from .home import home as home_blueprint
    # app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app


# debug = os.environ.get('FLASK_DEBUG', False)
# app, db = create_app(debug=debug)

config_name = os.getenv('FLASK_CONFIG')
if config_name is None:
    config_name = 'production'
app = create_app(config_name)


from priv import *
from case import *


if __name__ == "__main__":
    # app = create_app()
    app.run()
