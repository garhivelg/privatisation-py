#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


import os
import logging


from d2logger import getHandler


def run_app(debug=False):
    app = Flask(__name__)
    app.config.from_object('config')

    Session(app)

    db = SQLAlchemy(app)
    db.create_all()

    handler = getHandler()
    app.logger.addHandler(handler)
    if debug:
        app.logger.setLevel(logging.DEBUG)

    # app.run(debug=debug)

    return app, db


debug = os.environ.get('FLASK_DEBUG', False)
app, db = run_app(debug=debug)
print("Debug is %s" % (app.debug))


from priv import *
from case import *


if __name__ == "__main__":
    from priv.models.lookup import load
    load()

    app.logger.info("Starting Server")
    app.logger.info("Debug mode is %s", app.debug)
    from priv.models.lookup import CITIES
    app.logger.debug("CITIES=%s", CITIES)

    # app.run(debug=debug)
    app.run()
