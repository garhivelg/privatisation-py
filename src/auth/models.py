from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(16), index=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.login)