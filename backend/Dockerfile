FROM python:3.8-buster AS prod-stage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Use non-root user
ARG USERNAME=backenduser

# Create non-root user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
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
WORKDIR /code

# Copy dependency configuration
COPY --chown=$USERNAME:$USERNAME ./pyproject.toml ./poetry.lock* ./

# Install poetry and poetry dependencies
ENV POETRY_HOME=$HOMEDIR/.poetry
RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=$POETRY_HOME python \
    && ln -s $POETRY_HOME/bin/poetry $LOCALBIN/poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Copy project files
COPY --chown=$USERNAME:$USERNAME ./ ./

FROM prod-stage AS dev-stage

# Install dev dependencies
USER $USERNAME
RUN poetry install --no-root
# ARG SKIP_DEV_DEPS
# RUN bash -c "if [[ $SKIP_DEV_DEPS != 'true' ]] ; then poetry install --no-root ; fi"

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
