# eventvr-web

## Exit Codes

- 4190 - Forced guest dequeue by supervisor
- 4150 - Forced guest dequeue by guest

## Useful Environment Variables

### Required

- PGPASSWORD
- SECRET_KEY

### Development

- PGPASSWORD
- DJANGO_SETTINGS_MODULE
- ALLOWED_HOSTS
- INTERNAL_IPS

### Logging

- LOG_LEVEL_DJANGO
- LOG_LEVEL_EVENTVR
- LOG_FORMAT_STRING

### PostgreSQL Setup

```psql
CREATE DATABASE eventvr_database;
CREATE USER eventvr_db_admin WITH PASSWORD '';
ALTER ROLE eventvr_db_admin SET client_encoding TO 'utf8';
ALTER ROLE eventvr_db_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE eventvr_db_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventvr_database TO eventvr_db_admin;
```
