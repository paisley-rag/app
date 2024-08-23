#!/bin/bash

# Install postgresql
pipenv run sudo apt install postgresql postgresql-contrib

# load db details from .env
set -a
. ~/db/.env
set +a

# run init_pg.sql file as admin
PGPASSWORD=$PG_ADMIN_PASSWORD psql --host=$PG_HOST --port=$PG_PORT --username=$PG_ADMIN --password --dbname=postgres -f ~/db/setup_scripts/init_pg.sql

echo "PostgreSQL setup completed successfully."
