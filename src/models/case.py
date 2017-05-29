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
    register_id = db.Column(db.ForeignKey('register.id'))
    book_id = db.Column(db.String(8))
    book_num = db.Column(db.Integer)
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})
