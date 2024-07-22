#! /bin/bash

set -a
. ./.env
set +a

# Note:  --password will PROMPT the user to enter a password to login
#           - check .env file for the password

psql --host=$HOST --port=$PORT --username=$USERNAME --password --dbname=$DBNAME
