from app import db
from models import Record, Case


from test import PrivTestCase
from faker import Factory


import random


class RecordTestCase(PrivTestCase):
    def setUp(self):
        PrivTestCase.setUp(self)
        self.fake = Factory.create('ru_RU')

    def fake_record(self):
        record = Record(
            book_id=self.fake.pyint(),
            reg_num=self.fake.pyint(),
            reg_id=self.fake.pyint(),
            city_id=self.fake.pyint(),
        )
        db.session.add(record)
        db.session.commit()
        return record

    def show_record(self, record):
        print("ID", record.id)
        print(record.book_id)
        print(record.reg_num)
        print(record.reg_id)
        print(record.city_id)
        print(record.addr_type)
        print(record.addr_name)
        print(record.addr_build)
        print(record.addr_flat)
        print(record.owner)
        print(record.owner_init)
        print(record.owner_firstname)
        print(record.owner_middlename)
        print(record.base_id)
        print(record.base_date)
        print(record.reg_date)
        print(record.comment)
        print(record.case)

    def test_get_book(self):
        record = self.fake_record()
        self.assertEqual(record.get_book(), record.case)

    def test_get_reg(self):
        reg_num = self.fake.pyint()
        book_num = self.fake.pyint()

        reg = "0/%s" % (reg_num)
        record = self.fake_record()
        record.reg_num = reg_num
        record.case = None
        self.assertEqual(record.get_reg(), reg)

        reg = "%s/%s" % (book_num, reg_num)
        case = Case()
        case.book_num = book_num
        db.session.add(case)
        db.session.commit()
        record = self.fake_record()
        record.reg_num = reg_num
        record.case = case
        db.session.add(record)
        db.session.commit()
        self.assertEqual(record.get_reg(), reg)

    def test_get_reg_int(self):
        reg_num = self.fake.pyint()
        book_num = self.fake.pyint()
        reg_id = "%s/%s" % (book_num, reg_num)
        reg = "%s%s" % (book_num, reg_num)
        reg_int = int(reg)

        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = str(reg_num)
        self.assertEqual(record.get_reg_int(), 1)

        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id + reg_id
        self.assertEqual(record.get_reg_int(), 1)

        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id
        self.assertEqual(record.get_reg_int(), reg_num)

        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id + self.fake.pystr()
        self.assertEqual(record.get_reg_int(), reg_num)

        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = "%d/%s" % (reg_num, self.fake.pystr())
        self.assertEqual(record.get_reg_int(), 1)

    def test_get_city(self):
        from models.lookup import load
        load()

        from models.lookup import CITIES

        city_id = random.randrange(1, len(CITIES))
        city = CITIES[city_id]
        record = self.fake_record()
        record.city_id = city_id
        self.assertEqual(record.get_city(), CITIES[city_id])

        city_id = self.fake.pyint()
        record = self.fake_record()
        record.city_id = city_id
        self.assertEqual(record.get_city(), 'г. Луганск')

        city_id = -self.fake.pyint()
        record = self.fake_record()
        record.city_id = city_id
        self.assertEqual(record.get_city(), '')

        city_id = self.fake.pystr()
        record = self.fake_record()
        record.city_id = city_id
        self.assertEqual(record.get_city(), '')

    def test_get_addr(self):
        from models.lookup import load
        load()

        record = self.fake_record()
        record.addr_name = ''
        self.assertEqual(record.get_addr(), "Адрес не указан")

        street_name = self.fake.street_title()
        building_number = ''
        flat_number = ''
        addr = "г. Луганск,  %s %s" % (street_name, building_number)
        record = self.fake_record()
        record.addr_name = street_name
        record.addr_build = building_number
        record.addr_flat = flat_number
        self.assertEqual(record.get_addr(), addr)

        street_name = self.fake.street_title()
        building_number = self.fake.building_number()
        flat_number = ''
        addr = "г. Луганск,  %s %s" % (street_name, building_number)
        record = self.fake_record()
        record.addr_name = street_name
        record.addr_build = building_number
        record.addr_flat = flat_number
        self.assertEqual(record.get_addr(), addr)

        street_name = self.fake.street_title()
        building_number = self.fake.building_number()
        flat_number = self.fake.building_number()
        addr = "г. Луганск,  %s %s/%s" % \
            (street_name, building_number, flat_number)
        record = self.fake_record()
        record.addr_name = street_name
        record.addr_build = building_number
        record.addr_flat = flat_number
        self.assertEqual(record.get_addr(), addr)

    def test_get_owner(self):
        last_name = ''

        owner = "Неизвестен"
        record = self.fake_record()
        record.owner = last_name
        self.assertEqual(record.get_owner(), owner)

        last_name = self.fake.last_name()
        init = ""
        owner = "%s %s" % (
            last_name,
            init,
        )
        record = self.fake_record()
        record.owner = last_name
        record.owner_init = init
        self.assertEqual(record.get_owner(), owner)

        last_name = self.fake.last_name()
        init = "%s.%s." % (
            self.fake.first_name()[0],
            self.fake.middle_name()[0],
        )
        owner = "%s %s" % (
            last_name,
            init,
        )
        record = self.fake_record()
        record.owner = last_name
        record.owner_init = init
        self.assertEqual(record.get_owner(), owner)

    def test_random(self):
        for i in range(10):
            record = self.fake_record()
            self.assertEqual(record.generate_random(), None)

    def test_normalize(self):
        reg_num = None
        reg_id = ''
        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id
        record.normalize()
        self.assertEqual(record.reg_num, reg_num)

        reg_num = self.fake.pyint()
        reg_id = ''
        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id
        record.normalize()
        self.assertEqual(record.reg_num, reg_num)

        reg_num = None
        reg_id = str(self.fake.pyint())
        record = self.fake_record()
        record.reg_num = reg_num
        record.reg_id = reg_id
        record.normalize()
        self.assertEqual(str(record.reg_num), reg_id)

    def test_export(self):
        record = self.fake_record()
        export = record.export()
        self.assertEqual(export.get("book", dict()).get("id"), 0)

        case = Case()
        db.session.add(case)
        db.session.commit()
        record = self.fake_record()
        record.case = case
        export = record.export()
        self.assertEqual(export.get("book", dict()).get("id"), case.id)
