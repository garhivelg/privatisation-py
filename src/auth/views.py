from flask import flash, g, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from app import app, db
from .forms import LoginForm, UserForm
from .models import User


@app.route("/login",  methods=["GET", "POST"])
def login():
    """
    Вход в систему
    """
    if g.user is not None and g.user.is_authenticated:
        return redirect("/record")
    form = LoginForm()
    if form.validate_on_submit():
        if not form.login:
            flash('Вход не выполнен')
            return redirect(url_for('login'))
        user = User.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Вход не выполнен')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me)
        flash("Вход выполнен успешно!")
        return redirect(request.args.get('next') or url_for("list_records"))
    return render_template("auth/login.html", title="Вход", form=form)


@app.route("/logout")
@login_required
def logout():
    """
    Выход из системы
    """
    logout_user()
    return redirect(url_for('login'))


@app.route("/users", methods=["GET", "POST"])
@login_required
def list_users():
    """
    Показать список пользователей
    """
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    page = request.args.get('page', 1)

    q = User.query

    app.logger.debug(str(q))
    count = q.count()
    try:
        page = int(page)
    except ValueError:
        page = 1
    users = q.paginate(page, 50)
    return render_template("auth/list.html", users=users, page=page, count=count)


@app.route("/user/<int:user_id>")
@login_required
def edit_user(user_id):
    """
    Редактировать пользователя
    """
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user is None:
        flash("Пользователь не найден")
        return redirect(url_for("list_users"))

    form = UserForm(obj=user)
    return render_template(
        "auth/user.html",
        user=user,
        form=form,
        action=url_for('save_user', user_id=user.id)
    )


@app.route("/user/add")
@login_required
def add_user():
    """
    Добавить нового пользователя
    """
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    user = User()
    form = UserForm(obj=user)
    return render_template(
        "auth/user.html",
        user=user,
        form=form,
        action=url_for('save_user', user_id=user.id)
    )


@app.route("/user/save", methods=["POST", ])
@app.route("/user/save/<int:user_id>", methods=["POST", ])
@login_required
def save_user(user_id=0):
    """
    Сохранить пользователя
    """
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    form = UserForm(request.form)
    if form.validate():
        user = User.query.get(user_id) or User()

        user.login = form.login.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.role = form.role.data

        if form.password.data:
            user.set_password(form.password.data)
        elif not user_id:
            flash("Пароль обязателен для заполнения")
            return redirect(url_for("add_user"))

        db.session.add(user)
        db.session.commit()
        flash("Данные успешно внесены")
        return redirect(url_for("list_users"))
    else:
        flash("Пожалуйста, перепроверьте данные")
        for field, errors in form.errors.items():
            for error in errors:
                f = getattr(form, field)
                flash("Ошибка в графе \"{}\" - {}".format(f.label.text, error))
        if user_id == 0:
            return redirect(url_for("add_user"))

    return redirect(url_for("edit_user", user_id=user_id))


@app.route("/user/del/<int:user_id>")
@login_required
def del_user(user_id=0):
    """
    Удалить пользователя
    """
    if not g.user or not g.user.is_authenticated or not g.user.is_admin:
        return redirect(url_for('index'))

    user = User.query.get(user_id)

    if user is not None:
        db.session.delete(user)
        db.session.commit()

        flash("Запись успешно удалена")
    return redirect(url_for('list_users'))
