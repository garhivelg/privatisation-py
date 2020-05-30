from flask import flash, g, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app import app
from .forms import LoginForm
from .models import User


@app.route("/login",  methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect("/record")
    form = LoginForm()
    if form.validate_on_submit():
        if not form.login:
            flash('Вход не выполнен')
            return redirect(url_for('login'))
        user = User.query.filter_by(login=form.login.data, password=form.password.data).first()
        if user is None:
            flash('Вход не выполнен')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me)
        flash("Вход выполнен успешно!")
        return redirect(request.args.get('next') or "/record")
    return render_template("auth/login.html", title="Вход", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
