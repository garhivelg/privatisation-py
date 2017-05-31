from app import app, db
from flask_testing import TestCase


class PrivTestCase(TestCase):
    def create_app(self):
        app.config.update({
            'SQLALCHEMY_DATABASE_URI': "sqlite://",
            'TESTING': True,
        })
        self.client = app.test_client()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
