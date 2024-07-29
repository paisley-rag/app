#!/bin/bash

# Install postgresql
pipenv run sudo apt install postgresql postgresql-contrib

# load db details from .env
set -a
# . ../.env
~/db/.env
set +a

# run init_pg.sql file as admin
psql --host=$PG_HOST --port=$PG_PORT --username=$PG_ADMIN --password --dbname=postgres -f init_pg.sql

echo "PostgreSQL setup completed successfully."
