#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


import os
import logging
from logging.handlers import RotatingFileHandler

from d2logger import Handler


def run_app(debug=False):
    app = Flask(__name__)
    app.config.from_object('config')

    Session(app)

    db = SQLAlchemy(app)
    db.create_all()

    log_config = app.config.get("LOG", dict())
    handler = RotatingFileHandler(
        log_config.get("FILENAME"),
        maxBytes=log_config.get("MAX_BYTES"),
        backupCount=log_config.get("BACKUP_COUNT"),
    )
    formatter = logging.Formatter(log_config.get("FORMAT"))    
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    return app, db


debug = os.environ.get('FLASK_DEBUG', False)
app, db = run_app(debug=debug)


from priv import *
from case import *


if __name__ == "__main__":
    # app.run(debug=debug)
    app.run()
