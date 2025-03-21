-- Connect to the default 'postgres' database as a superuser
\c postgres;

-- Create the user
CREATE USER timewise_dev WITH PASSWORD 'timewise_dev_pwd';

-- Create the database
CREATE DATABASE timewise_dev_db;

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE timewise_dev_db TO timewise_dev;

-- Connect to the newly created database
\c timewise_dev_db;

-- Grant all privileges on all tables in the schema to the user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO timewise_dev;

-- Grant all privileges on all sequences in the schema to the user
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO timewise_dev;

-- Grant all privileges on all functions in the schema to the user
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO timewise_dev;