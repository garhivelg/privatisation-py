#!/bin/bash
coverage run --source=./ --omit=run_server.py run_tests.py
coverage report
coverage html -d ../htmlcov
