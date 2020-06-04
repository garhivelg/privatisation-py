# -*- coding:utf-8 -*-
from app import db
from priv.models.lookup import get_street, get_city, get_book
from case.models.facility import *
from case.models.case import *


class Record(db.Model):
    """
    Модель приватизационной записи
    """
    id = db.Column(db.Integer, primary_key=True)
    # book_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey("case.id"))
    reg_num = db.Column(db.Integer)
    reg_id = db.Column(db.String(8), info={'label': "Регистрационный №"})
    city_id = db.Column(db.Integer)
    addr_type = db.Column(db.Integer)
    addr_name = db.Column(db.String(64))
    addr_build = db.Column(db.String(8))
    addr_flat = db.Column(db.String(16))
    owner = db.Column(db.String(64))
    owner_init = db.Column(db.String(8))
    owner_firstname = db.Column(db.String(64))
    owner_middlename = db.Column(db.String(64))
    base_id = db.Column(
        db.String(8),
        nullable=True,
        info={'label': "Распоряжение №"}
    )
    base_date = db.Column(db.Date, nullable=True)
    reg_date = db.Column(
        db.Date,
        nullable=True,
        info={'label': "Дата регистрации"}
    )
    comment = db.Column(db.UnicodeText, info={'label': "Примечание"})

    case = db.relationship("Case")

    def get_book(self):
        """
        Приватизационное дело
        """
        return self.case

    def get_reg(self):
        """
        Регистрационный № в виде текста
        """
        if self.case:
            book_id = self.case.book_num
        else:
            book_id = 0
        return "{}/{}".format(
            book_id,
            self.reg_num,
        )

    def get_reg_int(self):
        """
        Регистрационный № в виде числа
        """
        parts = self.reg_id.split("/")
        if len(parts) != 2:
            return 1
        try:
            res = int(''.join(c for c in parts[-1] if c.isdigit()))
        except ValueError:
            res = 1
        return res

    def get_city(self):
        """
        Населенный пункт
        """
        try:
            city_id = int(self.city_id)
        except (TypeError, ValueError):
            city_id = 0

        if city_id <= 0:
            return ''
        return get_city(city_id)

    def get_addr(self, full=True):
        """
        Адрес
        """
        if not self.addr_name:
            return "Адрес не указан"

        addr = "{} {}".format(
            get_street(self.addr_type),
            self.addr_name
        )

        city = self.get_city()
        if city:
            addr = ', '.join([city, addr])

        if not full:
            return addr

        flat_num = self.addr_build
        if self.addr_flat:
            flat_num = flat_num + "/" + self.addr_flat

        addr += " " + flat_num
        return addr

    def get_owner(self):
        """
        Владелец
        """
        if not self.owner:
            return "Неизвестен"

        return "{} {}".format(
            self.owner,
            self.owner_init,
        )

    def generate_random(self):
        """
        Заполнить запись случайными данными
        """
        from .lookup import BOOKS, CITIES, STREETS
        import random
        # self.book_id = random.randrange(len(BOOKS))
        self.reg_num = random.randrange(0, 4000)
        self.reg_id = self.get_reg()
        if random.randint(0, 10) == 0:
            self.reg_id = self.reg_id + 'а'
        self.reg_num = int(''.join(c for c in self.reg_id if c.isdigit()))

        if len(CITIES):
            self.city_id = random.randrange(len(CITIES))
        else:
            self.city_id = 0
        if len(STREETS):
            self.addr_type = random.randrange(0, len(STREETS))
        else:
            self.addr_type = 0
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
        """
        Нормализация записи
        """
        if self.reg_num is None:
            if self.reg_id:
                self.reg_num = int(''.join(c for c in self.reg_id if c.isdigit()))

    def export(self):
        """
        Экспорт записи
        """
        if self.case:
            book_id = self.case.id
        else:
            book_id = 0
        return {
            "id": self.id,
            "book": {
                "id": book_id,
                "name": get_book(book_id),
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

    def import_yml(self, data=dict()):
        """
        Импорт записи
        """
        book = data.get('book', dict())
        addr = data.get('addr', dict())
        owner = data.get('owner', dict())
        book_id = book.get('id')
        if book_id:
            self.book_id = book_id
        self.reg_num = data.get('reg_num')
        self.reg_id = data.get('reg_id')

        self.city_id = addr.get('city', dict()).get('id')
        self.addr_type = addr.get('street', dict()).get('type_id')
        self.addr_name = addr.get('street', dict()).get('name')
        self.addr_build = addr.get('addr_build')
        self.addr_flat = addr.get('addr_flat')

        self.owner_init = owner.get('owner_init')
        self.owner = owner.get('owner')

        self.base_id = data.get('base_id')
        self.base_date = data.get('base_date')
        self.reg_date = data.get('reg_date')
        self.comment = data.get('comment')


class Sort:
    """
    Способ сортировки
    """
    title = ""

    def sort(self, query):
        """
        Добавить сортировку к запросу
        """
        query.order_by(None)


ORDER_BY = {
    "reg_id": {
        "title": "Регистрационный №",
        "order": {
            "asc": [Record.book_id.asc(), Record.reg_num.asc()],
            "desc": [Record.book_id.desc(), Record.reg_num.desc()],
        },
    },
    "addr": {
        "title": "Адрес",
        "order": {
            "asc": [Record.city_id.asc(), Record.addr_name.asc(), Record.addr_type.asc(), Record.addr_build.asc(), Record.addr_flat.asc()],
            "desc": [Record.city_id.desc(), Record.addr_name.desc(), Record.addr_type.desc(), Record.addr_build.desc(), Record.addr_flat.desc()],
        },
    },
    "owner": {
        "title": "Владелец",
        "order": {
            "asc": [Record.owner.asc(), Record.owner_init.asc()],
            "desc": [Record.owner.desc(), Record.owner_init.desc()],
        },
    },
    "base_id": {
        "title": "Основание",
        "order": {
            "asc": [Record.base_id.asc(), ],
            "desc": [Record.base_id.desc(), ],
        },
    },
}
