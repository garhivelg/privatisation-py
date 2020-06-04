import os
from datetime import timedelta


class Config(object):
    """
    Common configuration
    """
    # Корневая папка
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Ключ безопасности
    SECRET_KEY = "some key"
    # Тип сессии
    SESSION_TYPE = "filesystem"
    # Файл с данными сессии
    SESSION_FILE_DIR = os.path.join(BASE_DIR, "tmp")

    # Файл с данными сессии
    LOG = {
        "FILENAME": os.path.join(BASE_DIR, "log", "privatisation.log"),
        "MAX_BYTES": 1024 * 1024,
        "BACKUP_COUNT": 10,
        "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
    }

    # Интервал создания резервной копии
    BACKUP_TIME = timedelta(minutes=30)
    # Путь к БД
    DB_PATH = os.path.join(BASE_DIR, "db")
    # Путь к резервной копии БД
    BACKUP_PATH = os.path.join(DB_PATH, "backup")
    # Файл БД
    DB_FILENAME = "privatisation.db"
    # Файл резервной копии
    BACKUP_FILENAME = "privatisation-%s.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # URL БД
    SQLALCHEMY_DATABASE_URI = "sqlite:////%s/%s" % (DB_PATH, DB_FILENAME)


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    # Режим отладки
    DEBUG = True
    # Режим логирования запросов в БД
    SQLALCHEMY_ECHO = True
    # Режим логирования шаблонов
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    # Режим отладки
    DEBUG = False


class TestingConfig(Config):
    """
    Testing configuration
    """
    # Режим тестирования
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
