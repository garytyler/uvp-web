FROM python:3.9-buster AS python

FROM python AS base-stage

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USERNAME=backenduser \
    POETRY_HOME=/opt/.poetry \
    POETRY_VERSION=1.1.5

RUN useradd -ms /bin/bash $USERNAME

ARG WORKDIR=/srv/app/backend

COPY --chown=$USERNAME:$USERNAME ./pyproject.toml ./poetry.lock* $WORKDIR/

WORKDIR $WORKDIR

RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry \
    && poetry config --no-interaction virtualenvs.create false

FROM base-stage  AS install-stage

RUN poetry install --no-interaction --no-root --no-dev

FROM install-stage  AS install-dev-stage

RUN poetry install --no-interaction --no-root

FROM install-dev-stage AS dev-stage

RUN chmod go+x $POETRY_HOME/bin/poetry

RUN groupadd docker \
    && usermod -aG docker $USERNAME

RUN apt-get update \
    && apt-get install --no-install-recommends -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

CMD [ "python", "manage.py", "runserver"]

FROM install-stage AS prod-stage

COPY --chown=$USERNAME:$USERNAME . .

USER $USERNAME

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./gunicorn_conf.py", "app.main:app" ]
