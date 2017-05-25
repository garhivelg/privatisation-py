#! /usr/bin/env python
# -*- coding:utf-8 -*-
from app import app


import os
import logging
# logconfig = {"format": "%(asctime)s: [%(levelname)s]:\t%(message)s"}
debug = os.environ.get('FLASK_DEBUG', False)
if debug:
    logging.getLogger().setLevel(logging.DEBUG)
    # logconfig["level"] = logging.DEBUG
    # logconfig["filename"] = "debug.log"
# logging.basicConfig(**logconfig)

if __name__ == "__main__":
    from models.lookup import load
    load()
    from models.lookup import CITIES
    print(CITIES)

    app.run(debug=debug)
