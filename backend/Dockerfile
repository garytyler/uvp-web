FROM python:3.9-buster AS python

FROM python AS install-stage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# define username
ENV USERNAME=backenduser

# Create non-root user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID ${USERNAME} \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# If poetry installs dependencies from a git repo, it will
# store them in /usr/local/src, so let it.
RUN chown $USERNAME:root /usr/local/src

# Set as non-root user
USER $USERNAME

# Set locations
ARG HOMEDIR=/home/$USERNAME
ARG LOCALBIN=$HOMEDIR/.local/bin

# Create local bin dir and add to path
RUN mkdir -p $LOCALBIN
ENV PATH=$LOCALBIN:${PATH}

# Set working dir
WORKDIR /srv/app/backend/

# Copy dependency configuration
COPY --chown=$USERNAME:$USERNAME ./pyproject.toml ./poetry.lock* ./

# Install poetry and poetry dependencies
ENV POETRY_HOME=$HOMEDIR/.poetry
ENV POETRY_NO_INTERACTION=1
RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=$POETRY_HOME python \
    && ln -s $POETRY_HOME/bin/poetry $LOCALBIN/poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

FROM install-stage  AS install-dev-stage

# Install dev dependencies
USER $USERNAME
RUN poetry install --no-root

FROM install-stage AS prod-stage

# Copy project files
COPY --chown=$USERNAME:$USERNAME ./ ./

FROM install-dev-stage AS dev-stage

# Use root user for installing dev software
USER root

# Give sudo privs to non-root user
RUN apt-get update \
    && apt-get install --no-install-recommends -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install broswer dependencies for testing with playwright
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

# Use non-root user
USER $USERNAME

# With non-root user, install browsers for testing with playwright
RUN python -m playwright install
