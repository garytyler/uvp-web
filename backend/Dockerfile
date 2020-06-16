FROM tiangolo/uvicorn-gunicorn:python3.8

ENV PYTHON_PROJECT_DIR=/app/backend/

WORKDIR $PYTHON_PROJECT_DIR

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && chmod 755 /opt/poetry/bin/poetry \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

# Create non-root user
ARG USERNAME=backend
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Configure poetry for non-root user
USER $USERNAME
RUN poetry config virtualenvs.create false
USER root

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* $PYTHON_PROJECT_DIR

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ \"$INSTALL_DEV\" == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./ $PYTHON_PROJECT_DIR
ENV PYTHONPATH=$PYTHON_PROJECT_DIR
ENV APP_MODULE="app.main:app"
