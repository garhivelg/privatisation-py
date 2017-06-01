from app import app


import shutil
import os
from datetime import datetime, timedelta


BACKUP_TIME = timedelta(minutes=30)
ROOT_PATH = os.path.abspath('..')
DB_FILENAME = "privatisation.db"


def copy_db(time):
    old_filename = DB_FILENAME
    new_filename = "privatisation-{}.db".format(time.strftime("%y-%m-%d-%H-%M"))
    shutil.copyfile(
        os.path.join(ROOT_PATH, "db", old_filename),
        os.path.join(ROOT_PATH, "db", "backup", new_filename),
    )
    app.logger.debug("Saved as {}".format(new_filename))


def backup(saved):
    time_now = datetime.now()
    if saved is None:
        return time_now

    delta = time_now - saved
    if delta < BACKUP_TIME:
        return saved

    copy_db(time_now)
    return time_now
