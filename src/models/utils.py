from models import Record


def add_filters(query, fields, no_street=False):
    for k, v in fields.items():
        if v is None:
            continue
        if not hasattr(Record, k):
            continue
        if isinstance(v, int):
            if v < 0:
                continue
        if isinstance(v, str):
            if not v:
                continue
        # print(k, type(v), "\"%s\"" % v)
        query = query.filter(getattr(Record, k).like(v))
    # if session.get("no_street", False):
    if no_street:
        print("NO STREET", no_street)
        query = query.filter(Record.addr_name.like(''))
    return query


def update_records(query, fields):
    updates = dict()
    for k, v in fields.items():
        if v is None:
            continue
        if not hasattr(Record, k):
            continue
        if isinstance(v, int):
            if v < 0:
                continue
        if isinstance(v, str):
            if not v:
                continue
        # print(k, type(v), "\"%s\"" % v)
        updates[k] = v
    if not updates:
        return 0
    return query.update(updates, synchronize_session='fetch')
