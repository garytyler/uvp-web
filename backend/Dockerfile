FROM python:3.9-buster AS python

FROM python AS install-stage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set target locations
ARG LOCALBIN=/home/root/.local/bin
RUN mkdir -p $LOCALBIN
ENV PATH=$LOCALBIN:${PATH}

# Set working dir
WORKDIR /srv/app/backend/

# Copy dependency configuration
COPY ./pyproject.toml ./poetry.lock* ./

# Install poetry and poetry dependencies
ENV POETRY_HOME=/home/root/.poetry
ENV POETRY_NO_INTERACTION=1
RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=$POETRY_HOME python \
    && ln -s $POETRY_HOME/bin/poetry $LOCALBIN/poetry \
    && poetry install --no-root --no-dev


# Set entrypoint for all stages
ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]

FROM install-stage AS prod-stage

# Copy project files
COPY ./ ./

# Execute production server
CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./gunicorn_conf.py", "app.main:app" ]

FROM install-stage  AS dev-setup-stage

# Install dev dependencies
RUN poetry install --no-root

# Install browser dependencies for testing with playwright
# See: https://github.com/microsoft/playwright/blob/master/docs/docker/Dockerfile.bionic
# WebKit dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libnotify4 \
    libxslt1.1 \
    libevent-2.1-6 \
    libgles2 \
    libvpx5 \
    libxcomposite1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libepoxy0 \
    libgtk-3-0 \
    libharfbuzz-icu0

# gstreamer and plugins to support video playback in WebKit.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav

# Chromium dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libxtst6

# Firefox dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-glib-1-2 \
    libxt6

# With non-root user, install browsers for testing with playwright
RUN poetry run python -m playwright install

FROM dev-setup-stage AS dev-stage

# Copy project files
COPY ./ ./

CMD [ "python", "manage.py", "runserver" ]
