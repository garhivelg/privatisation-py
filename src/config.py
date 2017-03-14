import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/privatisation.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = "some key"
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "../tmp"
