#!/bin/bash

# Source the .env file to load existing environment variables, ignoring comments and empty lines
if [ -f ~/db/.env ]; then
	export $(grep -v '^#' ~/db/.env | xargs)
fi

# Install postgresql
DEBIAN_FRONTEND=noninteractive pipenv run sudo apt install postgresql postgresql-contrib -y

# load db details from .env
set -a
. ~/db/.env
set +a

# run init_pg.sql file as admin
export PGPASSWORD=$PG_ADMINPW
psql --host=$PG_HOST --port=$PG_PORT --username=$PG_ADMIN --dbname=postgres \
	-v pg_database=$PG_DATABASE -v pg_user=$PG_USER -v pg_password=$PG_PASSWORD -f ~/db/setup_scripts/init_pg.sql

echo "PostgreSQL setup completed successfully."
