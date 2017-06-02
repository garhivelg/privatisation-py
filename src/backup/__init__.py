from app import app


import shutil
import os
from datetime import datetime


def copy_db(time):
    old_filename = app.config.get("DB_FILENAME", "db")
    new_filename = app.config.get("BACKUP_FILENAME") % (time.strftime("%y-%m-%d-%H-%M"))
    shutil.copyfile(
        os.path.join(app.config.get("DB_PATH", "."), old_filename),
        os.path.join(app.config.get("BACKUP_PATH", "."), new_filename),
    )
    app.logger.debug("Saved as {}".format(new_filename))


def backup(saved):
    time_now = datetime.now()
    if saved is None:
        return time_now

    delta = time_now - saved
    if delta < app.config.get("BACKUP_TIME"):
        return saved

    copy_db(time_now)
    return time_now
