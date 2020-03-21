-- This script must be executed as the admin postgres user.
-- This script should not have to be manually executed,
-- because it will automatically be executed correctly
-- by the container if the attached PGDATA volume is empty.
CREATE USER dev_user WITH PASSWORD 'dev';
CREATE DATABASE dev_db;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO dev_user;
-- By default only the admin user can use pg_read_binary_file functions
GRANT EXECUTE ON FUNCTION pg_read_binary_file(text,bigint,bigint,boolean) TO dev_user;
GRANT EXECUTE ON FUNCTION pg_read_binary_file(text,bigint,bigint) TO dev_user; 
GRANT EXECUTE ON FUNCTION pg_read_binary_file(text) TO dev_user;