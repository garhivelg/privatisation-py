#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, redirect
# from flask import g, render_template, redirect, session
from flask.helpers import url_for
from app import app, db


@app.route("/")
def index():
    return redirect(url_for("list_records"))


@app.route("/record")
def list_records():
    from models import Record
    records = Record.query.order_by(Record.book_id.asc(), Record.reg_num.asc()).all()
    return render_template("index.html", records=records)


@app.route("/record/<int:record_id>")
def edit_record(record_id):
    from models import Record
    record = Record.query.get(record_id)
    return render_template("record.html", record=record)


@app.route("/record/add")
def add_record():
    import random
    from models.lookup import BOOKS
    book_id = random.randrange(len(BOOKS))
    print(book_id)

    from models import Record
    # from sqlalchemy.orm.exc import NoResultFound
    last = Record.query.filter_by(book_id=book_id).order_by(Record.reg_num.desc()).first()
    reg_id = 1
    if last is not None:
        if last.reg_num is not None:
            reg_id = last.reg_num + 1

    record = Record()
    record.book_id = book_id
    record.reg_id = reg_id
    record.reg_num = reg_id
    db.session.add(record)
    db.session.commit()

    return redirect(url_for("edit_record", record_id=record.id))
    # from models import Record
    # record = Record.query.get(record_id)
    # return render_template("record.html", record=record)


@app.route("/random")
@app.route("/random/<int:records>")
def random(records=1):
    from models import Record

    for i in range(records):
        r = Record()
        r.generate_random()

        db.session.add(r)
    db.session.commit()
    return redirect(url_for("list_records"))
