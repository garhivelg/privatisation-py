from app import db


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund = db.Column(db.String(4))
    register = db.Column(db.String(4))
    description = db.Column(db.UnicodeText)


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_id = db.Column(db.ForeignKey('register.id'))
    book_id = db.Column(db.String(8))
    book_num = db.Column(db.Integer)
    description = db.Column(db.UnicodeText)
