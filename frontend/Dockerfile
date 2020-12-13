FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as install-stage

# Create target directory
RUN mkdir --parents /srv/app/frontend && chown -R node:node /srv/app/frontend

# Use node user preconfigured by node image
USER node

# Set workdir to service destination
WORKDIR /srv/app/frontend

# COPY package.json package-lock.json /tmp/
COPY --chown=node:node package.json yarn.lock ./

# RUN npm install
RUN yarn config set yarn-offline-mirror ~/packages-cache
RUN yarn install

FROM install-stage as dev-stage

# Give sudo permissions to preconfigured node user
USER root
RUN apt-get update \
    && apt-get install --no-install-recommends -y sudo \
    && echo node ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/node \
    && chmod 0440 /etc/sudoers.d/node

# Use node user preconfigured by node image
USER node

# ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]
CMD [ "npm", "run", "serve", "--", "--host=0.0.0.0", "--port=80"]

FROM install-stage as build-stage

COPY . .

WORKDIR /srv/app/frontend

# Compile build
CMD [ "npm", "run", "build" ]

FROM nginx as prod-stage

# Copy build to server container
COPY --from=build-stage /srv/app/frontend/dist /app/

# Copy nginx configuration to server container
COPY nginx.conf /etc/nginx/nginx.conf
