#!/bin/bash

while read -r requirement; do
	echo "INSTALLING $requirement"
	su -c 'PIPENV_PIPFILE=/home/ubuntu/db/Pipfile pipenv run pip install $requirement --verbose' ubuntu >>/home/ubuntu/setup.log 2>&1
done </home/ubuntu/db/requirements.txt
