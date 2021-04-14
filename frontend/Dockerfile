FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as base-stage

ENV USERNAME=node

ARG WORKDIR=/srv/app/frontend

COPY --chown=$USERNAME:$USERNAME package.json yarn.lock $WORKDIR/

WORKDIR $WORKDIR

USER $USERNAME

RUN yarn config set yarn-offline-mirror ~/packages-cache \
    && yarn install

FROM base-stage as dev-stage

USER root

RUN apt-get update \
    && apt-get install --no-install-recommends -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

CMD [ "npm", "run", "serve"]

FROM install-stage as build-stage

COPY --chown=$USERNAME:$USERNAME . .

USER $USERNAME

CMD [ "npm", "run", "build" ]

FROM nginx as prod-stage

ARG WORKDIR

COPY --from=build-stage $WORKDIR/dist /app/

COPY nginx.conf /etc/nginx/nginx.conf
