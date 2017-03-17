#! /usr/bin/env python
# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields.html5 import DateField

from models.lookup import BOOKS, CITIES, STREETS


class RecordForm(FlaskForm):
    book_id = SelectField("Дело №",
                          choices=list(enumerate(BOOKS)),
                          coerce=int,
                          )
    reg_id = StringField("Регистрационный №", validators=[DataRequired(), Length(max=8)])

    full_addr = StringField("Адрес")
    city_id = SelectField("Населенный пункт",
                          choices=list(enumerate(CITIES)),
                          coerce=int,
                          )
    addr_type = SelectField("Вид улицы",
                            choices=list(enumerate(STREETS)),
                            coerce=int,
                            )
    addr_name = StringField("Название улицы", validators=[Length(max=64), ])
    addr_build = StringField("Дом", validators=[Length(max=8), ])
    addr_flat = StringField("Квартира", validators=[Length(max=16), ])

    full_owner = StringField("Владелец")
    owner = StringField("Фамилия", validators=[Length(max=64), ])
    owner_init = StringField("И.О.", validators=[Length(max=8), ])

    base_id = IntegerField("Распоряжение №")
    base_date = DateField('Дата распоряжения', format='%Y-%m-%d', validators=[Optional(), ])

    reg_date = DateField('Дата регистрации', format='%Y-%m-%d', validators=[Optional(), ])
    comment = TextAreaField('Примечание')
