SHELL := /bin/bash
include ../.env
export

env:
	pip install -r requirements/local.txt  > /dev/null

run:
	@echo "Running service..."
	python package/run.py

test: env
	@echo "Running unit tests..."
	coverage run --source=package setup.py test ${module} && \
	coverage html && \
	coverage report
	@echo
	@echo "Flake8 errors in code ----------------"
	@echo
	@echo "--------------------------------------"
	@python -m flake8 --max-line-length=180 --exclude .git,__pycache__,.eggs,build
	@echo "OK, no flake8 errors in code"
	@echo "--------------------------------------"
