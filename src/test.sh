#!/bin/bash
coverage run --source=./ run_tests.py
coverage report
coverage html -d ../htmlcov
