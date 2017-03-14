#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, redirect
# from flask import g, render_template, redirect, session
from flask.helpers import url_for

from app import app, db


@app.route("/")
def index():
    from models import Record
    records = Record.query.order_by(Record.book_id.asc(), Record.reg_num.asc()).all()
    return render_template("index.html", records=records)


@app.route("/random")
@app.route("/random/<int:records>")
def random(records=1):
    from models.lookup import BOOKS, CITIES, STREETS
    from models import Record
    import random

    for i in range(records):
        r = Record()
        r.generate_random()

        db.session.add(r)
    db.session.commit()
    return redirect(url_for("index"))
