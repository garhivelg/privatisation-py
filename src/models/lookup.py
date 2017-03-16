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

CITIES = [
    "г. Луганск",
    "г. Луганск",
    "Александровск",
    "пос. Юбилейный",
    "пос.Дзержинского",
    "пос.Промжилстрой",
    "пос. Дзержинског",
]

BOOKS = range(1, 25)


def get_street(street_id=None):
    if street_id not in range(1, len(STREETS) + 1):
        street_id = 0
    return STREETS[street_id]


def get_city(city_id=None):
    if city_id not in range(1, len(CITIES) + 1):
        city_id = 0
    return CITIES[city_id]


def get_book(book_id=None):
    if book_id not in range(1, len(BOOKS) + 1):
        book_id = 0
    return BOOKS[book_id]
