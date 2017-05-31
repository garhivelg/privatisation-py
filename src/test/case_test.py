from models import Register, Case


from test import PrivTestCase
from faker import Factory


class CaseTestCase(PrivTestCase):
    def setUp(self):
        PrivTestCase.setUp(self)
        self.fake = Factory.create('ru_RU')

    def test_register_title(self):
        f = "%s-%d"
        fund = self.fake.pystr()[:5]
        register = self.fake.pyint()
        case = Register(
            fund=fund,
            register=register,
        )
        self.assertEqual(case.title(f), f % (fund, register))

    def test_case_title(self):
        f = "%s-%s"

        book_num = self.fake.pyint()
        register = None
        case = Case(
            book_num=book_num,
            register=register,
        )
        self.assertEqual(case.title(f), f % ('', book_num))

        book_num = self.fake.pyint()
        register = Register(
            fund=self.fake.pystr()[:5],
            register=self.fake.pyint(),
        )
        case = Case(
            book_num=book_num,
            register=register,
        )
        self.assertEqual(case.title(f), f % (register, book_num))

        book_num = None
        register = Register(
            fund=self.fake.pystr()[:5],
            register=self.fake.pyint(),
        )
        case = Case(
            book_num=book_num,
            register=register,
        )
        self.assertEqual(case.title(f), f % (register, 1))
