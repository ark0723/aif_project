-- init.sql

SET @db_user = '${DB_USER}';
SET @db_password = '${DB_PASSWORD}';

-- Update authentication method for the specified user
ALTER USER @db_user IDENTIFIED WITH mysql_native_password BY @db_password;

