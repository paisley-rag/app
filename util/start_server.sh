#!/bin/bash
export PIPENV_PIPFILE=/home/ubuntu/db/Pipfile
export WORKON_HOME=/root/.local/share/virtualenvs/db-grdQ2Ybz
export PYTHONPATH=$(pipenv --venv)/bin
exec sudo pipenv run python -m db.server

