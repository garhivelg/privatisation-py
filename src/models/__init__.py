# -*- coding:utf-8 -*-
from app import db
from models.lookup import get_street, get_city, get_book


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

    def get_book(self):
        return get_book(self.book_id)

    def get_reg(self):
        return "{}/{}".format(
            get_book(self.book_id),
            self.reg_id,
        )

    def get_addr(self):
        addr = "{} {} {}/{}".format(
            get_street(self.addr_type),
            self.addr_name,
            self.addr_build,
            self.addr_flat,
        )

        try:
            city_id = int(self.city_id)
        except TypeError:
            city_id = 0

        if city_id > 1:
            addr = ' '.join([get_city(city_id), addr])
        return addr

    def get_owner(self):
        return "{} {}".format(
            self.owner,
            self.owner_init,
        )

    def generate_random(self):
        from models.lookup import BOOKS, CITIES, STREETS
        import random
        self.book_id = random.randrange(len(BOOKS))
        self.reg_id = str(random.randrange(0, 4000))
        if random.randint(0, 10) == 0:
            self.reg_id = self.reg_id + 'а'
        self.reg_num = int(''.join(c for c in self.reg_id if c.isdigit()))

        self.city_id = random.randrange(len(CITIES))
        self.addr_type = random.randrange(len(STREETS))
        self.addr_name = "Ленина"
        self.addr_build = random.randrange(1, 100)
        self.addr_flat = random.randrange(1, 100)
        self.owner = "Ленина"
        self.owner_init = "А.А."
        self.base_id = random.randrange(0, 4000)
        # base_date = db.Column(db.Date)
        # reg_date = db.Column(db.Date, nullable=True)
        self.normalize()

    def normalize(self):
        self.reg_num = int(''.join(c for c in self.reg_id if c.isdigit()))
