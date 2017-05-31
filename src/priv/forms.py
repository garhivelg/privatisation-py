from flask_wtf import FlaskForm
from wtforms import StringField  # , TextAreaField, SelectField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory

from .models import Record
from case.models import Case


from app import db


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class RecordForm(ModelForm):
    case = QuerySelectField(
        "Дело №",
        query_factory=lambda: Case.query.all(),
        allow_blank=True,
    )
    full_addr = StringField("Адрес")
    full_owner = StringField("Владелец")
    class Meta:
        model = Record
