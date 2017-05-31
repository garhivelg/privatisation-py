#! /usr/bin/env python
# -*- coding:utf-8 -*-
from app import app


import os
import logging


from d2logger import getHandler


debug = os.environ.get('FLASK_DEBUG', False)
if __name__ == "__main__":
    from priv.models.lookup import load
    load()
    from priv.models.lookup import CITIES

    handler = getHandler()
    app.logger.addHandler(handler)
    if debug:
        app.logger.setLevel(logging.DEBUG)

    app.logger.info("Starting Server")
    app.logger.info("Debug mode is %s", debug)
    app.logger.debug("CITIES=%s", CITIES)

    app.run(debug=debug)
