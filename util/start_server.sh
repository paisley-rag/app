#!/bin/bash
export PIPENV_PIPFILE=/home/ubuntu/db/Pipfile
export PYTHONPATH=$(pipenv --venv)/bin
exec pipenv run python -m db.server