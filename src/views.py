#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template
# from flask import g, render_template, redirect, session
# from flask.helpers import url_for

from app import app
# from models import pc


@app.route("/")
def index():
    return render_template("index.html")
