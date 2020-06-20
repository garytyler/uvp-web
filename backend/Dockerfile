FROM python:3.8-buster AS base-stage

# Use non-root user
ARG USERNAME=backenduser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update
USER $USERNAME

# Set home dir
ARG HOMEDIR=/home/$USERNAME

# Set local bin dir
ARG LOCALBIN=$HOMEDIR/.local/bin
RUN mkdir -p $LOCALBIN
ENV PATH=$LOCALBIN:${PATH}

# Install poetry
ENV POETRY_HOME=$HOMEDIR/.poetry
RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=$POETRY_HOME python \
    && ln -s $POETRY_HOME/bin/poetry $LOCALBIN/poetry
ENV PATH=$HOMEDIR/.local/bin:${PATH}

# Set working dir
WORKDIR /app/backend

# Install python dependencies
COPY ./pyproject.toml ./poetry.lock* /app/backend/
RUN poetry install --no-root --no-dev

# Copy app files
COPY ./ /app/backend/

# Configure server
ENV HOST="0.0.0.0"
ENV PORT="8000"

FROM base-stage AS prod-stage

# Configure server
ENV APP_MODULE="app.main:app"
ENV GUNICORN_CONF="./gunicorn_conf.py"
ENV WORKER_CLASS="uvicorn.workers.UvicornWorker"

# Start production server
CMD ["/bin/bash", "-c", "$(poetry env info -p)/bin/gunicorn -k $WORKER_CLASS -c $GUNICORN_CONF $APP_MODULE"]

FROM base-stage AS dev-stage

# Install development dependencies
RUN poetry install --no-root

# Start development server
CMD ["/bin/bash", "-c", "$(poetry env info -p)/bin/uvicorn --reload --host=$HOST --port=$PORT app.main:app"]
