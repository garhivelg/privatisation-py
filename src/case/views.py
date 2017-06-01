from flask import render_template, redirect, flash
from flask.helpers import url_for


from app import app, db


from .forms import CaseForm, RegisterForm, FacilityForm
from .models import Register, Case, Facility


@app.route("/registers")
def list_registers():
    items = Register.query.all()

    return render_template(
        "list.html",
        items=[
            [
                i,
                # url_for("list_cases", register_id=i.id),
                url_for("edit_register", register_id=i.id)
            ] for i in items
        ],
        add=url_for("edit_register"),
    )


@app.route("/register/edit/<int:register_id>", methods=["GET", "POST", ])
@app.route("/register/edit/<string:fund_title>/<int:fund_register>")
@app.route("/register/add", methods=["GET", "POST", ])
def edit_register(register_id=None, fund_title=None, fund_register=None):
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
        return redirect(url_for("list_registers"))

    app.logger.debug(form.errors)
    return render_template(
        "edit_register.html",
        form=form,
        register=register,
        items=Case.query.filter(Case.register == register)
    )


@app.route("/facilities")
def list_facilities():
    items = Facility.query.all()

    return render_template(
        "list.html",
        items=[
            [
                i,
                url_for("edit_facility", facility_id=i.id)
            ] for i in items
        ],
        add=url_for("edit_facility"),
    )


@app.route("/facility/edit/<int:facility_id>", methods=["GET", "POST", ])
@app.route("/facility/add", methods=["GET", "POST", ])
def edit_facility(facility_id=None):
    if facility_id is not None:
        facility = Facility.query.get_or_404(facility_id)
    else:
        facility = Facility()
    form = FacilityForm(obj=facility)

    if form.validate_on_submit():
        form.populate_obj(facility)
        db.session.add(facility)
        if facility.id:
            flash("Предприятие изменено")
        else:
            flash("Предприятие добавлено")
        db.session.commit()
        return redirect(url_for("list_facilities"))

    app.logger.debug(form.errors)
    return render_template(
        "edit_facility.html",
        form=form,
        facility=facility,
        items=Case.query.filter(Case.facility == facility)
    )


@app.route("/register/<int:register_id>/cases")
@app.route("/register/<string:fund_title>/<int:fund_register>/cases")
@app.route("/cases")
def list_cases(register_id=None, fund_title=None, fund_register=None):
    q = Case.query
    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first()
        q = q.filter(Case.register_id == register.id)
    elif register_id is not None:
        app.logger.debug(q)
        q = q.filter(Case.register_id == register_id)
        app.logger.debug(q)
    cases = q.all()

    items = [("Все", url_for("list_records", book=-1)), ] + [
        [
            i,
            url_for("list_records", book=i.id),
            url_for("edit_case", case_id=i.id),
        ] for i in cases
    ]

    app.logger.debug(items)
    return render_template(
        "list.html",
        items=items,
        add=url_for("edit_case"),
    )


@app.route("/case/edit/<int:case_id>", methods=["GET", "POST", ])
@app.route("/case/edit/<string:fund_title>/<int:fund_register>/<int:case_num>")
@app.route("/case/add/<int:register_id>", methods=["GET", "POST", ])
@app.route("/case/add", methods=["GET", "POST", ])
def edit_case(
    case_id=None,
    case_num=None,
    fund_title=None,
    fund_register=None,
    register_id=0
):

    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
        case = Case.query \
            .filter(Case.register_id == register.id) \
            .filter(Case.case_num == case_num) \
            .first_or_404()
    elif case_id is not None:
        case = Case.query.get_or_404(case_id)
    else:
        case = Case()
    form = CaseForm(obj=case)

    if form.validate_on_submit():
        form.populate_obj(case)
        case.register_id = form.register.data.id
        case.facility_id = form.facility.data.id
        db.session.add(case)
        if case.id:
            flash("Опись изменена")
        else:
            flash("Опись добавлена")
        db.session.commit()
        return redirect(url_for("list_cases"))

    if register_id:
        register = Register.query.get(register_id)
        form.register.data = register
    app.logger.debug(form.errors)

    return render_template("case.html", form=form, case=case)
