from flask.helpers import url_for
from test import PrivTestCase


class UrlTestCase(PrivTestCase):
    def test_index(self):
        rv = self.client.get(url_for('index'))
        self.assertRedirects(rv, url_for('list_records'))

    def test_list_records(self):
        rv = self.client.get(url_for('list_records'))
        assert b'No entries here so far' in rv.data

    def test_edit_record(self):
        rv = self.client.get(url_for('edit_record', record_id=15))
        assert b'No entries here so far' in rv.data

    def test_add_record(self):
        rv = self.client.get(url_for('add_record'))
        assert b'No entries here so far' in rv.data

    def test_empty_db(self):
        rv = self.client.get('/')
        assert b'No entries here so far' in rv.data
