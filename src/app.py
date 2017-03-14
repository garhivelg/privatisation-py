#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
app.config.from_object('config')

Session(app)

from views import *
# from web import models

# from db import db_session
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
