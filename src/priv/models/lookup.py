# -*- coding:utf-8 -*-
# from app import app


STREETS = []
CITIES = []
BOOKS = range(25)
STREETNAMES = []


def load():
    """
    Загрузить данные из файлов
    """
    from os import path
    from app import app
    DB_PATH = app.config.get('DB_PATH', '..')

    global CITIES
    with open(path.join(DB_PATH, "cities.txt"), encoding="utf-8") as f:
        CITIES = f.read().splitlines()

    global STREETS
    with open(path.join(DB_PATH, "streets.txt"), encoding="utf-8") as f:
        STREETS = f.read().splitlines()

    global STREETNAMES
    with open(path.join(DB_PATH, "streetnames.txt"), encoding="utf-8") as f:
        STREETNAMES = f.read().splitlines()


def set_street(street_name=""):
    """
    Добавить улицу в список если ее там нет
    """
    from os import path
    from app import app
    DB_PATH = app.config.get('DB_PATH', '..')

    global STREETS
    if street_name not in STREETS:
        STREETS.append(street_name)
        with open(path.join(DB_PATH, "streets.txt"), "w", encoding="utf-8") as f:
            for s in STREETS:
                f.write("{}\n".format(s))

    return STREETS.index(street_name)


def get_street(street_id=None):
    """
    Найти улицу по идентификатору
    """
    if street_id not in range(1, len(STREETS)):
        street_id = 0
    try:
        return STREETS[street_id]
    except IndexError:
        return "ERROR"


def find_street(street):
    """
    Найти идентификатор улицы по имени
    """
    try:
        return STREETS.index(street)
    except ValueError:
        return 0


def street_name(street):
    """
    Нормализовать название улицы
    """
    if not street:
        return "-"
    return street


def set_city(city_name=""):
    """
    Добавить населенный пункт в список если его там нет
    """
    from os import path
    from app import app
    DB_PATH = app.config.get('DB_PATH', '..')

    global CITIES
    if city_name not in CITIES:
        CITIES.append(city_name)
        with open(path.join(DB_PATH, "cities.txt"), "w", encoding="utf-8") as f:
            for c in CITIES:
                f.write("{}\n".format(c))

    return CITIES.index(city_name)


def find_city(city):
    """
    Найти идентификатор населенного пункта по имени
    """
    try:
        return CITIES.index(city)
    except ValueError:
        return 0


def get_city(city_id=None):
    """
    Найти населенный пункт по идентификатору
    """
    if city_id not in range(len(CITIES)):
        city_id = 0
    try:
        return CITIES[city_id]
    except IndexError:
        return "ERROR"


def get_book(book_id=None):
    """
    Найти номер регистрационного дела по идентификатору
    """
    if book_id not in range(1, len(BOOKS) + 1):
        book_id = 0
    return BOOKS[book_id]


def parse_street(s="", full=False):
    """
    Разбить адрес на составные части
    """
    import re
    parser = re.compile(r"(?:(.*),)?\s*(\w*\.)\s*(.*)")
    matches = parser.match(s)
    if matches:
        res = matches.groups()
    else:
        res = [None, None, s]

    addr = [res[2], None, None]
    if full:
        parser = re.compile(r"(.*),?\s+(\w+)/(\w+)")
        matches = parser.match(res[2])
        if matches:
            addr = matches.groups()

    return {
        'city_id': find_city(res[0]),
        'addr_type': find_street(res[1]),
        'addr_name': addr[0],
        'addr_build': addr[1],
        'addr_flat': addr[2],
    }


if not CITIES:
    load()
