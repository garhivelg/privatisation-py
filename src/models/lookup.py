# -*- coding:utf-8 -*-
STREETS = [
    "",
    "ул.",
    "кв.",
    "пер.",
    "гор.",
    "пр.",
    "прсп.",
    "пл.",
    "уч.",
    "мкр.",
    "пос.",
]

CITIES = []

BOOKS = range(25)


def load():
    global CITIES
    with open("../db/cities.txt", encoding="utf-8") as f:
        CITIES = f.read().splitlines()


def get_street(street_id=None):
    if street_id not in range(1, len(STREETS) + 1):
        street_id = 0
    return STREETS[street_id]


def find_street(street):
    try:
        return STREETS.index(street)
    except ValueError:
        return 0


def set_city(city_name=""):
    global CITIES
    if city_name not in CITIES:
        CITIES.append(city_name)
        with open("../db/cities.txt", "w", encoding="utf-8") as f:
            for c in CITIES:
                f.write("{}\n".format(c))

    return CITIES.index(city_name)


def get_city(city_id=None):
    if city_id not in range(len(CITIES)):
        city_id = 0
    return CITIES[city_id]


def get_book(book_id=None):
    if book_id not in range(1, len(BOOKS) + 1):
        book_id = 0
    return BOOKS[book_id]
