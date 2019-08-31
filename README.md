# eventvr-web

## Exit Codes

- 4190 - Forced guest dequeue by supervisor
- 4150 - Forced guest dequeue by guest

## Environment Variables

### Django settings

- SECRET_KEY
- DJANGO_SETTINGS_MODULE
- ALLOWED_HOSTS
- INTERNAL_IPS

### Database

- DATABASE_URL (See [DJ-Database-URL](https://github.com/jacobian/dj-database-url))
- CONN_MAX_AGE (Database max connection aga)

### Logging

- LOG_LEVEL_DJANGO
- LOG_LEVEL_EVENTVR
- LOG_FORMAT_STRING

### Channels

- ASGI_THREADS (See [Channels - Database Connections](https://channels.readthedocs.io/en/latest/topics/databases.html#database-connections))

## PostgreSQL Setup

```psql
CREATE DATABASE eventvr_database;
CREATE USER eventvr_db_admin WITH PASSWORD '';
ALTER ROLE eventvr_db_admin SET client_encoding TO 'utf8';
ALTER ROLE eventvr_db_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE eventvr_db_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventvr_database TO eventvr_db_admin;
```
