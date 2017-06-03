import os
from datetime import timedelta


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# basedir = os.getcwd()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/privatisation.db'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/privatisation.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = "some key"
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = os.path.join(basedir, "tmp")

# SERVER_NAME = "localhost"

LOG = {
    "FILENAME": os.path.join(basedir, "log", "privatisation.log"),
    "MAX_BYTES": 10000,
    "BACKUP_COUNT": 10,
    "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
}

BACKUP_TIME = timedelta(minutes=30)
DB_PATH = os.path.join(basedir, "db")
BACKUP_PATH = os.path.join(DB_PATH, "backup")
DB_FILENAME = "privatisation.db"
BACKUP_FILENAME = "privatisation-%s.db"
