#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import g, request, render_template, redirect, session, flash, jsonify
from flask.helpers import url_for
from app import app, db
from models.utils import add_filters, update_records
from backup import backup

from werkzeug.datastructures import MultiDict


@app.route("/")
def index():
    return redirect(url_for("list_records"))


@app.route("/record", methods=["GET", "POST"])
def list_records():
    session["saved"] = backup(session.get("saved"))

    from models import ORDER_BY
    order_id = request.args.get('order', None)
    order_dir = request.args.get('dir', None)
    order_desc = order_dir == 'desc'
    if order_id is not None:
        session["order"] = order_id
        order_dir = 'default'
    if order_dir is not None:
        session["order_desc"] = order_desc
    order_id = session.get("order")
    if session.get("order_desc"):
        order_dir = 'desc'
    else:
        order_dir = 'asc'

    links = dict()
    for k in ORDER_BY.keys():
        v = "asc"
        if k == order_id:
            if not order_desc:
                v = "desc"
        links[k] = url_for('list_records', order=k, dir=v)

    order = ORDER_BY.get(order_id, {"title": "", "order": {order_dir: [None]}})
    page = request.args.get('page', 1)
    g.order = order["title"]

    from models import Record
    q = Record.query
    q = q.order_by(*order["order"][order_dir])

    from forms import RecordForm
    form = request.form
    if form:
        session["filter"] = form.to_dict()

    filter_get = request.args.get('filter', True)
    if filter_get == "False":
        session["filter"] = dict()
        session["no_street"] = False

    filter_by = session.get("filter", dict())
    filter_book = request.args.get('book')
    if filter_book is not None:
        filter_by["book_id"] = int(filter_book)
        session["book_id"] = int(filter_book)
    filter_city = request.args.get('city')
    if filter_city is not None:
        filter_by["city_id"] = int(filter_city)
    filter_addr_type = request.args.get('addr_type')
    if filter_addr_type is not None:
        filter_by["addr_type"] = int(filter_addr_type)
    filter_street = request.args.get('street')
    if filter_street is not None:
        filter_by["addr_name"] = filter_street
    no_street = request.args.get('no_street')
    if no_street is not None:
        session["no_street"] = int(no_street)
    # print(filter_by)
    search = RecordForm(MultiDict(filter_by))

    q = add_filters(q, search.data, session.get("no_street"))

    print(str(q))
    count = q.count()
    records = q.paginate(int(page), 50)
    return render_template("record_list.html", records=records, page=page, links=links, search=search, count=count)


@app.route("/record/<int:record_id>")
def edit_record(record_id):
    from models import Record
    from forms import RecordForm
    record = Record.query.get(record_id)
    if record is None:
        flash("Запись не найдена")
        return redirect(url_for("list_records"))

    form = RecordForm(obj=record)
    form.page_id.data = request.args.get('page', 1)
    return render_template(
        "record.html",
        record=record,
        form=form,
        default_addr=record.get_addr(),
        default_owner=record.get_owner(),
        default_firstname="Имя",
        default_middlename="Отчество",
        action=url_for('save_record', record_id=record.id)
    )


@app.route("/record/add")
def add_record():
    book_id = session.get("book_id", 0)

    from models import Record
    from forms import RecordForm
    # from sqlalchemy.orm.exc import NoResultFound
    last = Record.query.filter_by(book_id=book_id).order_by(Record.reg_num.desc()).first()
    reg_id = 1
    if last is not None:
        if last.reg_num is not None:
            reg_id = last.get_reg_int() + 1

    record = Record()
    record.book_id = book_id
    record.reg_num = reg_id
    record.reg_id = record.get_reg()

    form = RecordForm(obj=record)
    return render_template(
        "record.html",
        record=record,
        form=form,
        default_addr="ул. Советская 85/25",
        default_owner="Фамилия И.О.",
        default_firstname="Имя",
        default_middlename="Отчество",
        action=url_for('save_record', record_id=record.id)
    )


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
        session["book_id"] = record.book_id

        flash("Данные успешно внесены")
        try:
            page_id = int(form.page_id.data)
        except ValueError:
            page_id = 1
        return redirect(url_for("list_records", page=page_id))
    else:
        flash("Пожалуйста, перепроверьте данные")
        for field, errors in form.errors.items():
            for error in errors:
                f = getattr(form, field)
                flash("Ошибка в графе \"{}\" - {}".format(f.label.text, error))
        if record_id == 0:
            return redirect(url_for("add_record"))

    return redirect(url_for("edit_record", record_id=record_id))


@app.route("/record/del/<int:record_id>")
def del_record(record_id=0):
    from models import Record
    record = Record.query.get(record_id)

    if record is not None:
        db.session.delete(record)
        db.session.commit()

        flash("Запись успешно удалена")

    return redirect(url_for("edit_record", record_id=record_id))


@app.route("/record/all", methods=["GET", "POST"])
def edit_all():
    from models import Record
    from forms import RecordForm
    save_form = RecordForm(request.form)

    form = RecordForm(MultiDict(session.get("filter", dict())))

    q = Record.query
    q = add_filters(q, form.data)

    if request.form:
        # record = Record.query.get(record_id)

        c = update_records(q, save_form.data)
        db.session.commit()

        flash("Данные успешно внесены")
        return redirect(url_for("list_records", filter=False))

    record = Record()

    return render_template(
        "record.html", record=record, form=form,
        default_addr="", default_owner="",
        hide_calc=True, action=url_for('edit_all'))


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
    items = [(-1, "Все"), ] + list(enumerate(BOOKS))
    return render_template("list.html", items=[
        [b,  url_for("list_records", book=i)] for i, b in items
    ])


@app.route("/list/streets")
def list_streets():
    from models.lookup import STREETS, street_name
    items = [(-1, "Все"), ] + list(enumerate(STREETS))
    return render_template("list.html", items=[
        [street_name(s), url_for("list_records", addr_type=i)] for i, s in items
    ])


@app.route("/list/cities")
def list_cities():
    from models.lookup import CITIES
    items = [(-1, "Все"), ] + list(enumerate(CITIES))
    return render_template("list.html", items=[
        [c, url_for("list_records", city=i)] for i, c in items
    ])


@app.route("/list/streetnames")
def list_street_names():
    from forms import RecordForm
    from models import Record
    from models.lookup import get_city, get_street
    records = [(
        "Все",
        url_for(
            "list_records",
            city=-1,
            addr_type=-1,
            street=None
        )

    ), ]
    search = RecordForm(MultiDict(session.get("filter", dict())))
    q = Record.query
    q = q.distinct(Record.addr_name).group_by(
        Record.city_id,
        Record.addr_type,
        Record.addr_name
    )
    # q = add_filters(q, search.data)
    for r in q:
        street = r.addr_name
        no_street = int(not street)
        records.append([
            ' '.join(
                [get_city(r.city_id), get_street(r.addr_type), r.addr_name]
            ),
            url_for(
                "list_records",
                city=r.city_id,
                addr_type=r.addr_type,
                street=r.addr_name,
                no_street=no_street
            )
        ])
    return render_template("list.html", items=records)


@app.route("/reindex")
def reindex(records=1):
    from models import Record

    records = Record.query.all()
    for r in records:
        r.normalize()
        print("Запись №{} успешно переиндексирована".format(r.reg_id))
        db.session.add(r)
    db.session.commit()
    return redirect(url_for("list_records"))


@app.route("/missing")
@app.route("/missing/<int:book_id>")
def missing(book_id=None):
    from models import Record
    from models.lookup import BOOKS

    if book_id is None:
        selected_books = BOOKS
    else:
        selected_books = [book_id, ]

    res = dict()
    for b in selected_books:
        q = Record.query.filter_by(book_id=b)
        first = q.order_by(Record.reg_num.asc()).first()
        last = q.order_by(Record.reg_num.desc()).first()
        count = q.count()
        res[b] = dict()

        if not last:
            print("BOOK#{} Empty!".format(b))
            continue

        res[b]['first'] = first.reg_id
        res[b]['last'] = last.reg_id
        if last.reg_num < b * 10000:
            multiplier = 1000
        else:
            multiplier = 10000
        first_id = b * multiplier
        expected = last.reg_num - first_id
        print("BOOK#{}\t{}-{} - {} of {}:\t{}".format(b, first.reg_id, last.reg_id, count, expected, last))
        missing = []
        doubled = []
        for i in range(1, expected + 1):
            reg_id = "{}/{}".format(b, i)
            records = Record.query.filter_by(reg_id=reg_id)
            if records.count() < 1:
                print("{} is missing!".format(reg_id))
                missing.append([reg_id, records.first()])
                continue
            if records.count() > 1:
                print("{} is doubled!".format(reg_id))
                doubled.append([reg_id, records.all()])
                continue
            print("{} is ok!".format(reg_id))

        res[b]['missing'] = missing
        res[b]['doubled'] = doubled
    return render_template("missing.html", books=res)


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
    from models.lookup import get_book, get_street, set_city
    with open(filename, 'r', encoding='cp1251') as f:
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

            r.book_id = book_id + 1
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
                    city = set_city(addr_data[1])
                    addr_data.append(city)
                    if addr_data[0]:
                        r.addr_type = int(addr_data[0])
                    r.city_id = city
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

    with open(filename + '.lst', 'r', encoding='cp1251') as f:
        while True:
            reg_id = f.readline()
            if not reg_id:
                break
            file_id = '../imports/' + f.readline()
            print(file_id)
            r = Record.query.filter_by(reg_id=reg_id).first()
            if not r:
                continue
            if not file_id:
                continue
            with open(file_id, 'r', encoding='cp1251') as comment_file:
                r.comment = comment_file.read()
            print(r.comment)
            db.session.add(r)
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


@app.route("/parse/addr", methods=["POST", ])
def parse_addr():
    addr = request.form.get('addr', "")
    import re
    parser = re.compile(r"(\w*\.)\s*(.*)\s+(\w+)/(\w+)")
    matches = parser.match(addr)
    if matches:
        res = matches.groups()
    else:
        res = [0, addr, "", ""]

    from models.lookup import find_street
    return jsonify(
        addr_type=find_street(res[0]),
        addr_name=res[1],
        addr_build=res[2],
        addr_flat=res[3],
    )


@app.route("/parse/owner", methods=["POST", ])
def parse_owner():
    owner = request.form.get('owner', "")
    import re
    parser = re.compile(r"(.*)\s+(\w\.\s*\w\.)")
    matches = parser.match(owner)
    if matches:
        res = matches.groups()
    else:
        res = [owner, ""]

    return jsonify(
        owner=res[0],
        owner_init=res[1],
    )


@app.route("/registers")
def list_registers():
    from models import Register
    items = Register.query.all()

    return render_template(
        "list.html",
        items=[
            [i, url_for("edit_register", register_id=i.id)] for i in items
        ],
        add=url_for("edit_register"),
    )


@app.route("/register/edit/<int:register_id>", methods=["GET", "POST", ])
@app.route("/register/edit/<string:fund_title>/<int:fund_register>")
@app.route("/register/add", methods=["GET", "POST", ])
def edit_register(register_id=None, fund_title=None, fund_register=None):
    from forms import RegisterForm
    from models import Register

    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
    elif register_id is not None:
        register = Register.query.get_or_404(register_id)
    else:
        register = Register()
    form = RegisterForm(obj=register)

    if form.validate_on_submit():
        form.populate_obj(register)
        db.session.add(register)
        if register.id:
            flash("Опись изменена")
        else:
            flash("Опись добавлена")
        db.session.commit()

    registers = Register.query.all()
    app.logger.debug(form.errors)
    app.logger.debug(registers)
    return render_template("edit_register.html", form=form, items=registers, register=register)


@app.route("/add/case", methods=["GET", "POST", ])
def add_case():
    from forms import CaseForm

    form = CaseForm()
    app.logger.debug(form)
    return render_template("case.html", form=form)
