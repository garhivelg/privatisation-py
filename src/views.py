#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template
# from flask import g, render_template, redirect, session
# from flask.helpers import url_for

from app import app, db


@app.route("/")
def index():
    from models import Record
    r = Record()
    r.book_id = 10
    db.session.add(r)
    db.session.commit()

    records = Record.query.all()
    return render_template("index.html", records=records)
