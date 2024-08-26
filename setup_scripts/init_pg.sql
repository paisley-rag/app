-- this file replaces init_pg.sql
-- we should have two tables, one for on-the-fly input/context/output entries
-- and one for benchmark data (with ~5 additional metrics), but to keep 
-- things easy for now there's a scored and unscored benchmark data table

-- Create a new user with a password
CREATE USER paisley WITH PASSWORD 'paisley_rules';

-- Create a new database
CREATE DATABASE paisley_evals;

-- Connect to the new database
\c paisley_evals

-- Create new tables
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB
);

CREATE TABLE benchmark_data (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE TABLE scored_benchmark_data (
    id SERIAL PRIMARY KEY,
    data JSONB
);

-- Grant privileges to the new user on the database and table
GRANT ALL PRIVILEGES ON DATABASE paisley_evals TO paisley;

GRANT ALL PRIVILEGES ON TABLE chat_history TO paisley;
GRANT ALL PRIVILEGES ON TABLE benchmark_data TO paisley;
GRANT ALL PRIVILEGES ON TABLE scored_benchmark_data TO paisley;

GRANT USAGE, SELECT ON SEQUENCE chat_history_id_seq TO paisley;
GRANT USAGE, SELECT ON SEQUENCE benchmark_data_id_seq TO paisley;
GRANT USAGE, SELECT ON SEQUENCE scored_benchmark_data_id_seq TO paisley;
