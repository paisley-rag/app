-- this file replaces init_pg.sql
-- we should have two tables, one for on-the-fly input/context/output entries
-- and one for benchmark data (with ~5 additional metrics), but to keep 
-- things easy for now there's a scored and unscored benchmark data table

-- Create a new user with a password
SET myapp.pg_user = :pg_user;
SET myapp.pg_password = :pg_password;

DO
$$
DECLARE
    pg_user TEXT := current_setting('myapp.pg_user');
    pg_password TEXT := current_setting('myapp.pg_password');
BEGIN
    EXECUTE format('CREATE USER %I WITH PASSWORD %L', pg_user, pg_password);
END
$$;
-- CREATE USER :pg_user WITH PASSWORD ':pg_password';

-- Create a new database
CREATE DATABASE :pg_database;

-- Connect to the new database
\c :pg_database

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
GRANT ALL PRIVILEGES ON DATABASE :pg_database TO :pg_user;

GRANT ALL PRIVILEGES ON TABLE chat_history TO :pg_user;
GRANT ALL PRIVILEGES ON TABLE benchmark_data TO :pg_user;
GRANT ALL PRIVILEGES ON TABLE scored_benchmark_data TO :pg_user;

GRANT USAGE, SELECT ON SEQUENCE chat_history_id_seq TO :pg_user;
GRANT USAGE, SELECT ON SEQUENCE benchmark_data_id_seq TO :pg_user;
GRANT USAGE, SELECT ON SEQUENCE scored_benchmark_data_id_seq TO :pg_user;
