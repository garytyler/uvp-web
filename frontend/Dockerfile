FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as install-stage

# Create target directory
RUN mkdir --parents /srv/app/frontend && chown -R node:node /srv/app/frontend

# Use node user provided by image
USER node

# Install node dependencies to a cache dir as node user
WORKDIR /tmp
COPY package.json package-lock.json /tmp/
RUN npm install

FROM install-stage as dev-stage

# Use node user provided by image
USER node

# Set workdir to service destination
WORKDIR /srv/app/frontend

# Copy repo contents
COPY . ./

# Copy node dependencies to service dir
RUN rm -rf ./node_modules && cp -af /tmp/node_modules ./

# Give sudo permissions to provided node user
USER root
RUN apt-get update \
    && apt-get install --no-install-recommends -y sudo \
    && echo node ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/node \
    && chmod 0440 /etc/sudoers.d/node
USER node

# Expose port
EXPOSE 8080

FROM dev-stage as build-stage

# Compile build
RUN npm run build

FROM nginx as prod-stage

# Copy build to server container
COPY --from=build-stage /srv/app/frontend/dist /app/

# Copy nginx configuration to server container
COPY nginx.conf /etc/nginx/nginx.conf
