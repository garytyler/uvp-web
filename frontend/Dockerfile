FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as install-stage

# Install node dependencies to cache dir
WORKDIR /tmp
COPY package.json package-lock.json /tmp/
RUN npm install

FROM install-stage as dev-stage

# Copy node dependencies to service dir
WORKDIR /srv/app/frontend
COPY . ./
RUN cp -a /tmp/node_modules /srv/app/frontend/

# Give sudo permissions to provided node user and change to node user
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
