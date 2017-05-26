#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
app.config.from_object('config')

Session(app)


# from db import db_session
db = SQLAlchemy(app)
db.create_all()

# import models
from models import *
from views import *

# migrate = Migrate(app, db)
