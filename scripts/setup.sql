CREATE TABLE IF NOT EXISTS random_data(id SERIAL PRIMARY KEY, timestamp TIMESTAMP, uuid VARCHAR(36));
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET listen_addresses = '*';
