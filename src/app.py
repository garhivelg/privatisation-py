#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


def run_app():
    app = Flask(__name__)
    app.config.from_object('config')

    Session(app)

    db = SQLAlchemy(app)
    db.create_all()
    return app, db


app, db = run_app()


from priv import *
from case import *
