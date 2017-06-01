import logging
from logging.handlers import RotatingFileHandler


LOG_FILENAME = "../log/privatisation.log"
LOG_LEVEL = logging.DEBUG
LOG_MAX_BYTES = 10000
LOG_BACKUP_COUNT = 10


def getHandler():
    handler = RotatingFileHandler(
        LOG_FILENAME,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT
    )
    # logconfig = {"format": "%(asctime)s: [%(levelname)s]:\t%(message)s"}
    # logconfig["level"] = logging.DEBUG
    # logconfig["filename"] = "debug.log"
    handler.setLevel(LOG_LEVEL)
    return handler
