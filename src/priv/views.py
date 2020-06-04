#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask import g, request, render_template, redirect, session, flash, jsonify
from flask.helpers import url_for
from flask_login import login_required
from datetime import datetime
from app import app, db
from priv.models.utils import add_filters, update_records
from backup import backup

from werkzeug.datastructures import MultiDict


def apply_order(order_dir=None):
    app.logger.debug("order_dir %s", order_dir)
    from priv.models import ORDER_BY
    order_id = request.args.get('order', None)
    order_desc = order_dir == 'desc'
    if order_id is not None:
        app.logger.debug("order_dir is not None %s", order_dir)
        session["order"] = order_id
        order_dir = 'default'
    if order_dir is not None:
        session["order_desc"] = order_desc
    order_id = session.get("order")
    app.logger.debug(session.get("order_desc"))
    if session.get("order_desc"):
        order_dir = 'desc'
    else:
        order_dir = 'asc'
    app.logger.debug("order_dir %s", order_dir)

    links = dict()
    for k in ORDER_BY.keys():
        v = "asc"
        if k == order_id:
            if not order_desc:
                v = "desc"
        links[k] = url_for('list_records', order=k, dir=v)

    order = ORDER_BY.get(order_id, {
        "title": "",
        "order": {order_dir: [None]}
    })
    return links, order, order_dir


@app.route("/")
def index():
    return render_template("priv/index.html", user=g.user, date=datetime.now())


@app.route("/record", methods=["GET", "POST"])
@login_required
def list_records():
    app.logger.debug("Saved at %s", session.get("saved"))
    session["saved"] = backup(session.get("saved"))

    order_dir = request.args.get('dir', None)
    links, order, order_dir = apply_order(order_dir)
    g.order = order["title"]

    page = request.args.get('page', 1)

    from priv.models import Record
    q = Record.query
    q = q.order_by(*order["order"][order_dir])

    from .forms import FilterForm
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
        book_id = int(filter_book)
        session["book_id"] = book_id
        filter_by["case"] = filter_book
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

    app.logger.debug(filter_by)
    search = FilterForm(MultiDict(filter_by))

    q = add_filters(q, search.data, session.get("no_street"))

    app.logger.debug(str(q))
    count = q.count()
    try:
        page = int(page)
    except ValueError:
        page = 1
    records = q.paginate(page, 50)
    return render_template("priv/list.html", records=records, page=page, links=links, search=search, count=count)


@app.route("/record/<int:record_id>")
@login_required
def edit_record(record_id):
    from .models import Record
    from .forms import RecordForm
    record = Record.query.get(record_id)
    if record is None:
        flash("Запись не найдена")
        return redirect(url_for("list_records"))

    form = RecordForm(obj=record)
    app.logger.debug(form.case.data)
    form.page_id.data = request.args.get('page', 1)
    return render_template(
        "priv/record.html",
        record=record,
        form=form,
        default_addr=record.get_addr(),
        default_owner=record.get_owner(),
        default_firstname="Имя",
        default_middlename="Отчество",
        default_lastname="Фамилия",
        default_init="И.О.",
        action=url_for('save_record', record_id=record.id)
    )


@app.route("/record/add")
@login_required
def add_record():
    book_id = session.get("book_id", 0)
    app.logger.debug("SESSION[book_id]=%s", session.get("book_id"))
    app.logger.debug("book_id=%s", book_id)

    from .models import Record, Case
    from .forms import RecordForm
    # from sqlalchemy.orm.exc import NoResultFound
    last = Record.query.filter_by(book_id=book_id).order_by(Record.reg_num.desc()).first()
    reg_id = 1
    if last is not None:
        if last.reg_num is not None:
            reg_id = last.get_reg_int() + 1

    record = Record()
    record.case = Case.query.get(book_id)
    record.reg_num = reg_id
    record.reg_id = record.get_reg()
    app.logger.debug("book_id=%s", record.case)

    form = RecordForm(obj=record)
    return render_template(
        "priv/record.html",
        record=record,
        form=form,
        default_addr="ул. Советская 85/25",
        default_owner="Фамилия И.О.",
        default_firstname="Имя",
        default_middlename="Отчество",
        default_lastname="Фамилия",
        default_init="И.О.",
        action=url_for('save_record', record_id=record.id)
    )


@app.route("/record/save", methods=["POST", ])
@app.route("/record/save/<int:record_id>", methods=["POST", ])
@login_required
def save_record(record_id=0):
    from .forms import RecordForm
    form = RecordForm(request.form)

    if form.validate():
        from priv.models import Record
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
@login_required
def del_record(record_id=0):
    from priv.models import Record
    record = Record.query.get(record_id)

    if record is not None:
        db.session.delete(record)
        db.session.commit()

        flash("Запись успешно удалена")

    return redirect(url_for("edit_record", record_id=record_id))


@app.route("/record/all", methods=["GET", "POST"])
@login_required
def edit_all():
    from .models import Record
    from .forms import RecordForm
    save_form = RecordForm(request.form)

    filter_data = session.get("filter", dict())
    if not filter_data:
        flash("Фильтр не установлен!")
        return redirect(url_for("list_records", filter=False))
    filter_data = MultiDict(filter_data)

    form = RecordForm(filter_data)

    q = Record.query
    q = add_filters(q, form.data)

    if request.form:
        # record = Record.query.get(record_id)

        app.logger.debug(q)
        app.logger.debug(save_form.data)
        data = save_form.data
        if save_form.case.data:
            data['book_id'] = save_form.case.data.id
            data['case'] = None
        app.logger.debug(data)
        c = update_records(q, data)
        db.session.commit()

        flash("Данные успешно внесены")
        return redirect(url_for("list_records", filter=False))

    record = Record()

    return render_template(
        "priv/record.html", record=record, form=form,
        default_addr="", default_owner="",
        hide_calc=True, action=url_for('edit_all'))


@app.route("/random")
@app.route("/random/<int:records>")
@login_required
def generate_random(records=1):
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    from priv.models import Record

    for i in range(records):
        r = Record()
        r.generate_random()

        db.session.add(r)
    db.session.commit()
    return redirect(url_for("list_records"))


@app.route("/list/books")
def list_books():
    from priv.models.lookup import BOOKS
    items = [(-1, "Все"), ] + list(enumerate(BOOKS))
    return render_template("priv/list_data.html", items=[
        [b,  url_for("list_records", book=i)] for i, b in items
    ])


@app.route("/list/streets")
def list_streets():
    from priv.models.lookup import STREETS, street_name
    items = [(-1, "Все"), ] + list(enumerate(STREETS))
    return render_template("priv/list_data.html", items=[
        [street_name(s), url_for("list_records", addr_type=i)] for i, s in items
    ])


@app.route("/list/cities")
def list_cities():
    from priv.models.lookup import CITIES
    items = [(-1, "Все"), ] + list(enumerate(CITIES))
    return render_template("priv/list_data.html", items=[
        [c, url_for("list_records", city=i)] for i, c in items
    ])


@app.route("/list/streetnames")
def list_street_names():
    from .forms import RecordForm
    from .models import Record
    from .models.lookup import get_city, get_street
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
    return render_template("priv/list_data.html", items=records)


@app.route("/list/streetnames.json")
def list_street_names_json():
    from .models.lookup import STREETNAMES, parse_street
    query = request.args.get('query', '')
    suggest = []
    for s in STREETNAMES:
        if query in s:
            suggest.append({
                'value': s,
                'data': parse_street(s),
            })
            app.logger.debug("%s:%s", query, suggest)

    return jsonify({
        "query": request.args.get('query', ''),
        "suggestions": suggest,
    })


@app.route("/reindex")
@login_required
def reindex(records=1):
    from priv.models import Record

    records = Record.query.all()
    for r in records:
        r.normalize()
        print("Запись №{} успешно переиндексирована".format(r.reg_id))
        db.session.add(r)
    db.session.commit()
    return redirect(url_for("list_records"))


@app.route("/missing")
@app.route("/missing/<int:book_id>")
@login_required
def missing(book_id=None):
    from case.models import Case
    from priv.models import Record

    if book_id is None:
        book_id = session.get('filter', dict()).get('case')

    if book_id is None:
        selected_books = Case.query.all()
    else:
        selected_books = [Case.query.get_or_404(book_id), ]

    res = dict()
    for b in selected_books:
        q = Record.query.filter_by(case=b)
        first = q.order_by(Record.reg_num.asc()).first()
        last = q.order_by(Record.reg_num.desc()).first()
        count = q.count()
        res[b] = dict()

        if not last:
            print("BOOK#{} Empty!".format(b))
            continue

        res[b]['first'] = first.reg_id
        res[b]['last'] = last.reg_id
        if last.reg_num < b.book_num * 10000:
            multiplier = 1000
        else:
            multiplier = 10000
        first_id = b.book_num * multiplier
        expected = last.reg_num - first_id
        print("BOOK#{}\t{}-{} - {} of {}:\t{}".format(b, first.reg_id, last.reg_id, count, expected, last))
        missing = []
        doubled = []
        for i in range(1, expected + 1):
            reg_id = "{}/{}".format(b.book_num, i)
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
@login_required
def export_yml():
    from priv.models import Record
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


def read_lst(filename):
    from priv.models import Record
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


def load_from_file(filename):
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    from case.models import Case
    from priv.models import Record
    from priv.models.lookup import get_book, get_street, set_city
    book_id = session.get('filter', dict()).get('case')
    try:
        book_id = int(book_id)
    except:
        book_id = None

    app.logger.debug(book_id)
    app.logger.debug(session)
    if book_id is None:
        selected_books = [book.id for book in Case.query.all()]
    else:
        selected_books = [book_id, ]

    app.logger.debug(selected_books)

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
            try:
                r.base_date = datetime.strptime(base_date_str, '%d.%m.%y')
            except ValueError:
                pass
            try:
                r.reg_date = datetime.strptime(reg_date_str, '%d.%m.%y')
            except ValueError:
                pass
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

            app.logger.debug("%s vs %s", r.book_id, selected_books)
            if r.book_id in selected_books:
                r.normalize()
                print("Запись №{} успешно импортирована".format(r.reg_id))
                db.session.add(r)
            else:
                app.logger.debug("Запись №%s из книги %s пропускается", r.reg_id, r.book_id)

            if not l:
                    break
    db.session.commit()

    try:
        read_lst(filename)
    except FileNotFoundError:
        pass

    db.session.commit()
    return True


def read_record(f):
    r = dict()
    r['book_id'] = int(f.readline())
    r['reg_id'] = f.readline().rstrip()

    r['addr_type'] = f.readline()
    r['addr_name'] = f.readline().rstrip()
    r['addr_build'] = f.readline().rstrip()
    r['addr_flat'] = f.readline().rstrip()

    r['owner'] = f.readline().rstrip()
    r['owner_init'] = f.readline().rstrip()
    r['base_id'] = f.readline().rstrip()

    from datetime import datetime
    base_date_str = f.readline().rstrip()
    reg_date_str = f.readline().rstrip()
    r['base_date'] = datetime.strptime(base_date_str, '%d.%m.%y')
    r['reg_date'] = datetime.strptime(reg_date_str, '%d.%m.%y')
    return r


def count_in_file(filename):
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    books = dict()
    d = []
    with open(filename, 'r', encoding='cp1251') as f:
        while True:
            tmp = f.readline()
            if not tmp:
                break
            record_id = int(tmp)
            r = read_record(f)
            l = f.readline()

            book_id = r.get('book_id', 0)
            books[book_id] = books.get(book_id, 0) + 1

            app.logger.debug("Запись №{} успешно прочитана".format(r.get('reg_id')))

            if not l:
                    break

    return books


@app.route("/import/files")
@login_required
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
    return render_template("priv/list_data.html", items=records)


@app.route("/import/count/files")
@login_required
def count_import_files():
    import os
    imports = '../imports'
    f = []
    filename = request.args.get('file', None)
    if filename:
        books = count_in_file(os.path.join(imports, filename))

        from case.models import Case
        items = [[
            "%d \"%s\" (записей: %s)" % (k, Case.query.get(k), v),
            url_for('list_records', book_id=k),
        ] for k, v in books.items()]
        return render_template("priv/list_data.html", items=items)

    records = []
    for file in os.listdir(imports):
        if file.endswith(".dat"):
            records.append([file, url_for('count_import_files') + "?file=" + file])
    return render_template("priv/list_data.html", items=records)


@app.route("/parse/addr", methods=["POST", ])
def parse_addr():
    addr = request.form.get('addr', "")

    from .models.lookup import parse_street
    return jsonify(parse_street(addr, full=True))


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
