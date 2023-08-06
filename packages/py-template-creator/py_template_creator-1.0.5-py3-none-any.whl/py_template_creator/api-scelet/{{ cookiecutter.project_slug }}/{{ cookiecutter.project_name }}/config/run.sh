#!/usr/bin/env bash

python {{cookiecutter.app_name}}/migrations/manage.py version_control
python {{cookiecutter.app_name}}/migrations/manage.py upgrade
{{cookiecutter.app_name}}
