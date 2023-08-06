#!/bin/sh
set -e  # Configure shell so that if one command fails, it exits
export TEST_DB=True
pip install -U pip
pip install -r /opt/app/requirements/test.txt
coverage erase
coverage run --source=package setup.py test
python -m flake8 --max-line-length=180 --exclude .git,__pycache__,.eggs,build
coverage report
coverage html
coverage-badge
