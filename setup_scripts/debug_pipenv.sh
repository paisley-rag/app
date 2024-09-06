#!/bin/bash

while read -r requirement; do
	echo "INSTALLING $requirement"
	cd /home/ubuntu/db && pipenv run pip install $requirement --verbose >>/home/ubuntu/setup.log 2>&1
done </home/ubuntu/db/requirements.txt
