from flask_login import UserMixin
from app import db


class Counter(db.Model, UserMixin):
    """
    Модель счетчика
    """
    id = db.Column(db.Integer, primary_key=True)
    remote_addr = db.Column(db.String(16), index=True, unique=True)
    first_visit = db.Column(db.DateTime())

    def __repr__(self):
        return '<Remote Addr {}>'.format(self.remote_addr)
