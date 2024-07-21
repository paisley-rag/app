#!/bin/bash

# Install postgresql
pipenv run sudo apt install postgresql postgresql-contrib

# Switch to the postgres user and run psql commands
sudo -u postgres psql <<EOF

-- Create a new user with a password
CREATE USER paisley WITH PASSWORD 'paisley_rules';

-- Create a new database
CREATE DATABASE paisley_evals;

-- Connect to the new database
\c paisley_evals

-- Create a new table
CREATE TABLE evals (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    output TEXT NOT NULL,
    context TEXT NOT NULL,
    answer_relevancy_score FLOAT NOT NULL
);

-- Grant privileges to the new user on the database and table
GRANT ALL PRIVILEGES ON DATABASE paisley_evals TO paisley;
GRANT ALL PRIVILEGES ON TABLE evals TO paisley;
GRANT USAGE, SELECT ON SEQUENCE evals_id_seq TO paisley;

EOF

echo "PostgreSQL setup completed successfully."
