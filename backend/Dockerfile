FROM python:3.8-buster AS base-stage

# Use non-root user
ARG USERNAME=backenduser

# Create non-root user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Set as non-root user
USER $USERNAME

# Set locations
ARG WORKDIR=/app/backend
ARG HOMEDIR=/home/$USERNAME
ARG LOCALBIN=$HOMEDIR/.local/bin

# Create local bin dir and add to path
RUN mkdir -p $LOCALBIN
ENV PATH=$LOCALBIN:${PATH}

# Set working dir
WORKDIR $WORKDIR

# Copy dependency configuration
COPY ./pyproject.toml ./poetry.lock* $WORKDIR

# Install poetry and poetry dependencies
ENV POETRY_HOME=$HOMEDIR/.poetry
RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=$POETRY_HOME python \
    && ln -s $POETRY_HOME/bin/poetry $LOCALBIN/poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Configure server
ENV HOST="0.0.0.0"
ENV PORT="8000"
ENV APP_MODULE="app.main:app"

FROM base-stage AS prod-stage

# Copy project files
COPY ./ $WORKDIR

# Start production server
CMD ["/bin/bash", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -c ./gunicorn_conf.py $APP_MODULE"]

FROM base-stage AS dev-stage

# Use non-root user for everything else
USER $USERNAME

# Install dev dependencies
RUN poetry install --no-root

# Use root user to install sudo and make non-root user a sudoer
USER root
RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Use non-root user for everything else
USER $USERNAME

# Install git
RUN sudo apt-get install git -y

# Start development server
CMD ["/bin/bash", "-c", "uvicorn --reload --host=$HOST --port=$PORT app.main:app"]
