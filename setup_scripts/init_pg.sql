-- this file replaces init_pg.sql
-- now we have two tables, one for on-the-fly input/context/output entries
-- and one for golden dataset values (with ~5 additional metrics)


-- Create a new user with a password
CREATE USER paisley WITH PASSWORD 'paisley_rules';

-- Create a new database
CREATE DATABASE paisley_evals2;

-- Connect to the new database
\c paisley_evals

-- Create new tables
CREATE TABLE running_evals (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB
);

CREATE TABLE batch_evals (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB
);

CREATE TABLE golden_dataset (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE TABLE scored_golden_dataset (
    id SERIAL PRIMARY KEY,
    data JSONB
);

-- Grant privileges to the new user on the database and table
GRANT ALL PRIVILEGES ON DATABASE paisley_evals2 TO paisley;

GRANT ALL PRIVILEGES ON TABLE running_evals TO paisley;
GRANT ALL PRIVILEGES ON TABLE batch_evals TO paisley;
GRANT ALL PRIVILEGES ON TABLE golden_dataset TO paisley;
GRANT ALL PRIVILEGES ON TABLE scored_golden_dataset TO paisley;

GRANT USAGE, SELECT ON SEQUENCE running_evals_id_seq TO paisley;
GRANT USAGE, SELECT ON SEQUENCE batch_evals_id_seq TO paisley;
GRANT USAGE, SELECT ON SEQUENCE golden_dataset_id_seq TO paisley;
GRANT USAGE, SELECT ON SEQUENCE scored_golden_dataset_id_seq TO paisley;
