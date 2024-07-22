#!/bin/bash

# Install postgresql
pipenv run sudo apt install postgresql postgresql-contrib

# Switch to the postgres user and run psql commands
sudo -u postgres psql << init_pg.sql

echo "PostgreSQL setup completed successfully."
