from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo
from .models import ROLE_USER, ROLE_ADMIN


class LoginForm(FlaskForm):
    """
    Форма входа в систему
    """
    login = StringField("Имя пользователя", validators=[DataRequired(message="Поле обязательно для заполнения")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Поле обязательно для заполнения")])
    remember_me = BooleanField("Запомнить меня", default=False)


class UserForm(FlaskForm):
    """
    Форма редактирования пользователя
    """
    login = StringField("Имя пользователя", validators=[DataRequired(message="Поле обязательно для заполнения")])
    name = StringField("Имя")
    surname = StringField("Фамилия")
    password = PasswordField("Пароль")
    verify_password = PasswordField("Повторите Пароль", validators=[EqualTo('password', message="Пароли не совпадают")])
    role = SelectField(
        "Права Доступа",
        choices=[
            (ROLE_USER, "Пользователь"),
            (ROLE_ADMIN, "Администратор"),
        ],
        coerce=int,
    )
