#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory

from models.lookup import BOOKS, CITIES, STREETS
from models import Case, Register


from app import db


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class RegisterForm(ModelForm):
    class Meta:
        model = Register


class CaseForm(ModelForm):
    register = QuerySelectField(
        "Register",
        get_label=lambda r: r.fund + ':' + r.register,
        query_factory=lambda: Register.query.all(),
        allow_blank=True,
    )

    class Meta:
        model = Case


class RecordForm(FlaskForm):
    book_id = SelectField("Дело №",
                          choices=[(-1, "Все"), ] + list(enumerate(BOOKS)),
                          coerce=int,
                          )
    reg_id = StringField("Регистрационный №", validators=[DataRequired(), Length(max=8)])

    full_addr = StringField("Адрес")
    city_id = SelectField("Населенный пункт",
                          choices=[(-1, "Все"), ] + list(enumerate(CITIES)),
                          coerce=int,
                          )
    addr_type = SelectField("Вид улицы",
                            choices=[(-1, "Все"), ] + list(enumerate(STREETS)),
                            coerce=int,
                            )
    addr_name = StringField("Название улицы", validators=[Length(max=64), ])
    addr_build = StringField("Дом", validators=[Length(max=8), ])
    addr_flat = StringField("Квартира", validators=[Length(max=16), ])

    full_owner = StringField("Владелец")
    owner = StringField("Фамилия", validators=[Length(max=64), ])
    owner_init = StringField("И.О.", validators=[Length(max=8), ])
    owner_firstname = StringField("Имя", validators=[Length(max=64), ])
    owner_middlename = StringField("Отчество", validators=[Length(max=64), ])

    base_id = StringField("Распоряжение №", validators=[Optional(), ])
    base_date = DateField('Дата распоряжения', format='%Y-%m-%d', validators=[Optional(), ])

    reg_date = DateField('Дата регистрации', format='%Y-%m-%d', validators=[Optional(), ])
    comment = TextAreaField('Примечание')

    page_id = HiddenField()
