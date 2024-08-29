#!/bin/bash
export PIPENV_PIPFILE=/home/ubuntu/db/Pipfile
export CELERYPATH=$(pipenv --venv)/bin
exec $CELERYPATH/celery -A db.celery.tasks worker -l info -E -f ~/celery.log
# cd ~/db && pipenv shell && $VIRTUAL_ENV/bin/celery -A db.celery.tasks worker -l info -f ~/celery.log