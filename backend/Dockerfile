# FROM tiangolo/uvicorn-gunicorn:python3.8 AS prod-stage
FROM python:3.8-buster AS prod-stage

# Create non-root user
ARG USERNAME=backend-user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Use non-root user
USER $USERNAME

# Set service base dir
ARG BASEDIR=/app/backend

# Set working dir
WORKDIR $BASEDIR

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

# Install prod dependencies
COPY ./pyproject.toml ./poetry.lock* $BASEDIR/
RUN poetry install --no-root --no-dev

# Copy app files
COPY ./ $BASEDIR/
ENV PYTHONPATH=$BASEDIR

# Configure server
ENV APP_MODULE="app.main:app"
ENV GUNICORN_CONF="./gunicorn_conf.py"
ENV WORKER_CLASS="uvicorn.workers.UvicornWorker"
ENV HOST="0.0.0.0"
ENV PORT="8000"

# Start production server
CMD ["/bin/bash", "-c", "$(poetry env info -p)/bin/gunicorn -k $WORKER_CLASS -c $GUNICORN_CONF $APP_MODULE"]

FROM prod-stage AS dev-stage

# Install development dependencies
RUN poetry install --no-root

# Start development server
CMD ["/bin/bash", "-c", "$(poetry env info -p)/bin/uvicorn --reload --host=$HOST --port=$PORT app.main:app"]
