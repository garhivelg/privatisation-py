from app import db


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund = db.Column(db.String(8), info={'label': "Фонд"})
    register = db.Column(db.Integer(), info={'label': "Опись"})
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    def title(self, format="ф. %s оп. %s"):
        return format % (self.fund, self.register)

    def __repr__(self):
        return self.title()


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    book_id = db.Column(db.String(8), info={'label': "Дело №"})
    book_num = db.Column(db.Integer, nullable=False, default=0)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    register = db.relationship("Register")
    facility = db.relationship("Facility")

    def title(self, format="%s д. %d"):
        if self.book_num is None:
            book_num = 1
        else:
            book_num = self.book_num
        if self.register:
            return format % (self.register, book_num)
        return format % ('', book_num)

    def __repr__(self):
        return self.title()
