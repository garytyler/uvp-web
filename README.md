# seevr-web

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/garytyler/seevr-web/tree/master)

## Useful environment variables

### Framework

- SECRET_KEY (Required)
- ALLOWED_HOSTS (Required for production)
  - Delimited by commas

### Database

- DATABASE_URL (Required for production)
  - See [DJ-Database-URL](https://github.com/jacobian/dj-database-url) for schema
- CONN_MAX_AGE
  - Database max connection age

### Logging

- LOG_LEVEL_DJANGO
- LOG_LEVEL_LIVE

### Channels

- ASGI_THREADS (See [Channels - Database Connections](https://channels.readthedocs.io/en/latest/topics/databases.html#database-connections))
- IN_MEMORY_CHANNEL_LAYER (For development only)

# Configuration

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_TEMPLATE_DEBUG

## Exit Codes

- 4190 - Forced guest dequeue by supervisor
- 4150 - Forced guest dequeue by guest
