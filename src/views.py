#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, render_template, redirect, flash
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
    return render_template("record_list.html", records=records)


@app.route("/record/<int:record_id>")
def edit_record(record_id):
    from models import Record
    from forms import RecordForm
    record = Record.query.get(record_id)
    if record is None:
        flash("Запись не найдена")
        return redirect(url_for("list_records"))

    form = RecordForm(obj=record)
    return render_template("record.html", record=record, form=form, default_addr=record.get_addr(), default_owner=record.get_owner())


@app.route("/record/add")
def add_record():
    import random
    from models.lookup import BOOKS
    book_id = random.randrange(len(BOOKS))

    from models import Record
    from forms import RecordForm
    # from sqlalchemy.orm.exc import NoResultFound
    last = Record.query.filter_by(book_id=book_id).order_by(Record.reg_num.desc()).first()
    reg_id = 1
    if last is not None:
        if last.reg_num is not None:
            reg_id = last.reg_num + 1

    record = Record()
    record.book_id = book_id
    record.reg_num = reg_id
    record.reg_id = record.get_reg()

    form = RecordForm(obj=record)
    return render_template("record.html", record=record, form=form, default_addr="ул. Советская 85/25", default_owner="Фамилия И.О.")


@app.route("/record/save", methods=["POST", ])
@app.route("/record/save/<int:record_id>", methods=["POST", ])
def save_record(record_id=0):
    from forms import RecordForm
    form = RecordForm(request.form)

    if form.validate():
        from models import Record
        record = Record.query.get(record_id)
        if record is None:
            record = Record()

        form.populate_obj(record)
        record.normalize()
        db.session.add(record)
        db.session.commit()

        flash("Данные успешно внесены")
    else:
        flash("Пожалуйста, перепроверьте данные")
        for field, errors in form.errors.items():
            for error in errors:
                f = getattr(form, field)
                flash("Ошибка в графе \"{}\" - {}".format(f.label.text, error))
        if record_id == 0:
            return redirect(url_for("add_record"))

    return redirect(url_for("edit_record", record_id=record_id))


@app.route("/random")
@app.route("/random/<int:records>")
def generate_random(records=1):
    from models import Record

    for i in range(records):
        r = Record()
        r.generate_random()

        db.session.add(r)
    db.session.commit()
    return redirect(url_for("list_records"))
