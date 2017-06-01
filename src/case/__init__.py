#! /usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session


def run_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Session(app)

    # from db import db_session
    db = SQLAlchemy(app)
    db.create_all()

    return app, db


if __name__ == "__main__":
    app, db = run_app()


# import models
from .models import *
from .views import *
