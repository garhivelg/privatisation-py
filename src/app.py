#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
# from flask_migrate import Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from config import app_config

import os
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(debug=False):
    """
    Создаем экземпляр Flask
    :param debug: включить режим отладки
    :return: экземпляр Flask
    """
    app = Flask(__name__)
    # app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    BASE_DIR = app.config.get('BASE_DIR', '../')
    app.template_folder = app.config.get('TEMPLATE_FOLDER', 'templates')
    app.static_folder = app.config.get('STATIC_FOLDER', 'static')

    # bootstrap = Bootstrap(app)
    session = Session(app)

    db.init_app(app)

    login_manager.init_app(app)
    # login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "login"

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
        """
        Показать страницу с сообщением об ошибке 404
        :param error: текст ошибки
        :return:
        """
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        """
        Показать страницу с сообщением об ошибке 403
        :param error: текст ошибки
        :return:
        """
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Показать страницу с сообщением об ошибке 500
        :param error: текст ошибки
        :return:
        """
        return render_template('errors/500.html', title='Server Error'), 500

    return app


# debug = os.environ.get('FLASK_DEBUG', False)
# app, db = create_app(debug=debug)

config_name = os.getenv('FLASK_CONFIG')
if config_name is None:
    config_name = 'production'
app = create_app(config_name)
manager = Manager(app)


from priv import *
from auth import *
from case import *
from counter import *
from priv.commands import *
from auth.commands import *


@app.before_request
def before_request():
    """
    Загружаем счетчики и пользователя в глобальный объект
    :return:
    """
    g.counter = update_counter()
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    """
    Загружаем пользователя из БД
    :return: учетная запись пользователя
    """
    return User.query.get(user_id)


if __name__ == "__main__":
    # app = create_app()
    app.run()
