# eventvr

## Environment Variables

### Required

- EVENTVR_DB_USER
- EVENTVR_DB_PASS

### Optional

- IN_MEMORY_CHANNEL_LAYER

## PostgreSQL Setup

```psql
CREATE DATABASE eventvr_database; CREATE USER eventvr_db_admin WITH PASSWORD '';
ALTER ROLE eventvr_db_admin SET client_encoding TO 'utf8';
ALTER ROLE eventvr_db_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE eventvr_db_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventvr_database TO eventvr_db_admin;
```
