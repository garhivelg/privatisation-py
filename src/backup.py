import shutil
import os
from datetime import datetime, timedelta


BACKUP_TIME = timedelta(minutes=5)


def copy_db(time):
    ROOT_PATH = os.path.abspath('..')
    old_filename = "privatisation.db"
    new_filename = "privatisation-{}.db".format(time.strftime("%y-%m-%d-%H-%M"))
    shutil.copyfile(
        os.path.join(ROOT_PATH, "db", old_filename),
        os.path.join(ROOT_PATH, "backup", new_filename),
    )
    print("Saved as {}".format(new_filename))


def backup(saved):
    time_now = datetime.now()
    if saved is None:
        return time_now

    delta = time_now - saved
    if delta < BACKUP_TIME:
        return saved

    copy_db(time_now)
    return time_now
