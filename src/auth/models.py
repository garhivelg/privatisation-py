from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model, UserMixin):
    """
    Модель пользователя
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(16), index=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    @property
    def title(self):
        """
        Имя пользователя
        """
        if self.name or self.surname:
            return " ".join([
                self.name,
                self.surname,
            ])
        return self.login

    @property
    def is_admin(self):
        """
        Пользователь является администратором
        """
        return self.role == ROLE_ADMIN

    def set_password(self, password):
        """
        Установить пароль
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Проверить пароль
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.title)
