#!/bin/bash

while read -r requirement; do
	echo "INSTALLING $requirement"
	pip install -r $requirement --verbose >>/home/ubuntu/setup.log 2>&1
done </home/ubuntu/db/requirements.txt
