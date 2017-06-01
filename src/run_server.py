#! /usr/bin/env python
# -*- coding:utf-8 -*-
from app import app


if __name__ == "__main__":
    app.logger.info("Running Server")
    app.logger.info("Debug mode is %s", app.debug)
    from priv.models.lookup import CITIES
    app.logger.debug("CITIES=%s", CITIES)

    app.run()
