import os
from datetime import timedelta


class Config(object):
    """
    Common configuration
    """
    # BASE_DIR = os.path.abspath(os.getcwd())
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    # STATIC_FOLDER = os.path.join(BASE_DIR, "static")

    SECRET_KEY = "some key"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(BASE_DIR, "tmp")

    # SERVER_NAME = "localhost"

    LOG = {
        "FILENAME": os.path.join(BASE_DIR, "log", "privatisation.log"),
        "MAX_BYTES": 1024 * 1024,
        "BACKUP_COUNT": 10,
        "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
    }

    BACKUP_TIME = timedelta(minutes=30)
    DB_PATH = os.path.join(BASE_DIR, "db")
    BACKUP_PATH = os.path.join(DB_PATH, "backup")
    DB_FILENAME = "privatisation.db"
    BACKUP_FILENAME = "privatisation-%s.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////%s/%s" % (DB_PATH, DB_FILENAME)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/privatisation.db')
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False


class TestingConfig(Config):
    """
    Testing configuration
    """
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
