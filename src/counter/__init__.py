import os
from datetime import datetime
from flask import request
from app import db
from .models import *


def __read_counters():
    if not os.path.exists("counters.txt"):
        return 1
    try:
        with open("counters.txt", "r") as f:
            return int(next(f))
    except ValueError:
        return 1


def update_counter():
    remote_addr = request.remote_addr
    exists = Counter.query.filter_by(remote_addr=remote_addr).count()
    if exists:
        return __read_counters()
    record = Counter(
        remote_addr=remote_addr,
        first_visit=datetime.now(),
    )
    db.session.add(record)
    db.session.commit()

    if os.path.exists("counters.txt"):
        try:
            with open("counters.txt", "r") as f:
                counter = int(next(f)) + 1
        except ValueError:
            counter = 1
    else:
        counter = 1

    with open("counters.txt", "w") as f:
        f.write(str(counter))

    return counter

