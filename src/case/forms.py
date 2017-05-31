from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory

from .models import Case, Register, Facility


from app import db


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class RegisterForm(ModelForm):
    class Meta:
        model = Register


class FacilityForm(ModelForm):
    class Meta:
        model = Facility


class CaseForm(ModelForm):
    register = QuerySelectField(
        "Опись",
        query_factory=lambda: Register.query.all(),
        allow_blank=True,
    )
    facility = QuerySelectField(
        "Предприятие",
        query_factory=lambda: Facility.query.all(),
        allow_blank=True,
    )

    class Meta:
        model = Case
