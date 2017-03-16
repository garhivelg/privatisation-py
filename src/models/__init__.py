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
            self.reg_num,
        )

    def get_city(self):
        try:
            city_id = int(self.city_id)
        except TypeError:
            city_id = 0

        if city_id > 1:
            return get_city(city_id)
        return ""

    def get_addr(self):
        if not self.addr_name:
            return "Адрес не указан"

        flat_num = self.addr_build
        if self.addr_flat:
            flat_num = flat_num + "/" + self.addr_flat

        addr = "{} {} {}".format(
            get_street(self.addr_type),
            self.addr_name,
            flat_num,
        )

        city = self.get_city()
        if city:
            addr = ' '.join([city, addr])
        return addr

    def get_owner(self):
        if not self.owner:
            return "Неизвестен"

        return "{} {}".format(
            self.owner,
            self.owner_init,
        )

    def generate_random(self):
        from models.lookup import BOOKS, CITIES, STREETS
        import random
        self.book_id = random.randrange(len(BOOKS))
        self.reg_num = random.randrange(0, 4000)
        self.reg_id = self.get_reg()
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

        from datetime import date, timedelta
        rand_date = random.randrange(3650) + 7300
        self.base_date = date.today() - timedelta(days=rand_date)

        # base_date = db.Column(db.Date)
        # reg_date = db.Column(db.Date, nullable=True)
        self.normalize()

    def normalize(self):
        if self.reg_num is None:
            if self.reg_id:
                self.reg_num = int(''.join(c for c in self.reg_id if c.isdigit()))

    def export(self):
        return {
            "id": self.id,
            "book": {
                "id": self.book_id,
                "name": get_book(self.book_id),
            },
            "reg_num": self.reg_num,
            "reg_id": self.reg_id,
            "addr": {
                "full": self.get_addr(),
                "city": {
                    "id": self.city_id,
                    "name": get_city(self.city_id),
                },
                "street": {
                    "type_id": self.addr_type,
                    "type": get_street(self.addr_type),
                    "name": self.addr_name,
                },
                "addr_build": self.addr_build,
                "addr_flat": self.addr_flat,
            },
            "owner": {
                "full": self.get_owner(),
                "owner": self.owner,
                "owner_init": self.owner_init,
            },
            "base_id": self.base_id,
            "base_date": self.base_date,
            "reg_date": self.reg_date,
            "comment":  self.comment,
        }
