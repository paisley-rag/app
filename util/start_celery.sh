#!/bin/bash
cd ~/db && pipenv shell && $VIRTUAL_ENV/bin/celery -A db.celery.tasks worker -l info -f ~/celery.log