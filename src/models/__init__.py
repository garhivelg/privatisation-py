from app import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    reg_num = db.Column(db.Integer)
    reg_id = db.Column(db.String(8))
    city_id = db.Column(db.Integer)
    addr_type = db.Column(db.Integer)
    addr_name = db.Column(db.String(64))
    addr_build = db.Column(db.String(8))
    addr_flat = db.Column(db.String(16))
    owner = db.Column(db.String(64))
    owner_init = db.Column(db.String(8))
    base_id = db.Column(db.String(8))
    base_date = db.Column(db.Date)
    reg_date = db.Column(db.Date, nullable=True)
    comment = db.Column(db.UnicodeText)
