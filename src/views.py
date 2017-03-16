#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, render_template, redirect, session, flash
# from flask import g, render_template, redirect, session
from flask.helpers import url_for
from app import app, db


@app.route("/")
def index():
    return redirect(url_for("list_records"))


@app.route("/record")
def list_records():
    order = request.args.get('order', None)
    if order is not None:
        session["order"] = order
    order = session["order"]

    from models import Record
    q = Record.query
    if order == 'book_id':
        q = q.order_by(Record.book_id.asc())
    elif order == 'reg_id':
        q = q.order_by(Record.book_id.asc(), Record.reg_num.asc())
    elif order == 'addr':
        q = q.order_by(Record.city_id.asc(), Record.addr_name.asc(), Record.addr_type.asc(), Record.addr_build.asc(), Record.addr_flat.asc())
    elif order == 'owner':
        q = q.order_by(Record.owner.asc(), Record.owner_init.asc())
    elif order == 'base_id':
        q = q.order_by(Record.base_id.asc())

    records = q.all()
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


@app.route("/list/books")
def list_books():
    from models.lookup import BOOKS
    return render_template("list.html", items=[[b,  "#"] for b in BOOKS])


@app.route("/list/streets")
def list_streets():
    from models.lookup import STREETS
    return render_template("list.html", items=[[s, "#"] for s in STREETS])


@app.route("/list/cities")
def list_cities():
    from models.lookup import CITIES
    return render_template("list.html", items=[[c, "#"] for c in CITIES])


@app.route("/list/streetnames")
def list_street_names():
    from models import Record
    from models.lookup import CITIES, STREETS
    records = []
    for r in Record.query.distinct(Record.addr_name).group_by(Record.city_id, Record.addr_type, Record.addr_name):
        records.append([' '.join([CITIES[r.city_id], STREETS[r.addr_type], r.addr_name]), "#"])
    return render_template("list.html", items=records)


@app.route("/export")
def export_yml():
    from models import Record
    import yaml
    records = Record.query.order_by(Record.book_id.asc(), Record.reg_num.asc()).all()

    from datetime import date
    from flask import make_response
    # response = make_response(yaml.dump(records))
    values = [r.export() for r in records]
    response = make_response(yaml.dump(values, default_flow_style=False))
    response.headers['Content-Type'] = 'text/yaml'
    response.headers['Content-Disposition'] = 'attachment; filename=' + date.today().strftime("%x") + '.yml'
    return response


def load_from_file(filename):
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    from models import Record
    from models.lookup import get_book, get_street, CITIES
    f = open(filename, 'r', encoding='cp1251')
    d = []
    while True:
        r = Record()

        tmp = f.readline()
        if not tmp:
            break

        record_id = int(tmp)
        book_id = int(f.readline()) - 1
        book = get_book(book_id)
        reg_id = f.readline().rstrip()

        r = Record.query.filter_by(reg_id=reg_id).first()
        if r is None:
            r = Record()

        r.book_id = book_id
        r.reg_id = reg_id
        addr_type = f.readline()
        r.addr_name = f.readline().rstrip()
        r.addr_build = f.readline().rstrip()
        r.addr_flat = f.readline().rstrip()
        r.city_id = 0
        try:
            r.addr_type = int(addr_type)
        except ValueError:
            addr_data = addr_type.rstrip().split(':')
            if len(addr_data) > 1:
                addr_data.append(CITIES.index(addr_data[1]))
                r.addr_type = int(addr_data[0])
                r.city_id = CITIES.index(addr_data[1])
            else:
                r.addr_type = 0
        street = get_street(r.addr_type)
        addr = [
            r.addr_type,
            r.city_id,
            r.addr_name,
            r.addr_build,
            r.addr_flat,
            street,
            r.get_addr(),
        ]
        r.owner = f.readline().rstrip()
        r.owner_init = f.readline().rstrip()
        owner = [
            r.owner,
            r.owner_init,
            r.get_owner(),
        ]
        r.base_id = f.readline().rstrip()

        from datetime import datetime
        base_date_str = f.readline().rstrip()
        reg_date_str = f.readline().rstrip()
        r.base_date = datetime.strptime(base_date_str, '%d.%m.%y')
        r.reg_date = datetime.strptime(reg_date_str, '%d.%m.%y')
        l = f.readline()

        d.append([
            record_id,
            [
                r.book_id,
                book,
            ],
            r.reg_id,
            addr,
            owner,
            r.base_id,
            [
                base_date_str,
                # base_date,
                r.base_date,
            ],
            [
                reg_date_str,
                # reg_date,
                r.reg_date,
            ],
        ])

        r.normalize()
        print("Запись №{} успешно импортирована".format(r.reg_id))
        db.session.add(r)

        if not l:
                break
    db.session.commit()
    return True


@app.route("/import/files")
def list_import_files():
    import os
    imports = '../imports'
    f = []
    filename = request.args.get('file', None)
    if filename:
        f = load_from_file(os.path.join(imports, filename))
        return redirect(url_for("list_records"))

    records = []
    for file in os.listdir(imports):
        # records.append(file)
        if file.endswith(".dat"):
            records.append([file, url_for('list_import_files') + "?file=" + file])
    return render_template("list.html", items=records)
