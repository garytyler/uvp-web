FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as base-stage

# Use non-root user
ARG USERNAME=frontenduser
RUN usermod -d /home/$USERNAME -l $USERNAME node

# Set service base dir
ARG SERVICEDIR=/app/frontend

# Install node dependencies to cache dir
WORKDIR /tmp
COPY package*.json /tmp/
RUN npm install

# Copy node dependencies to service dir
WORKDIR /app/frontend
COPY . /app/frontend/
RUN cp -a /tmp/node_modules /app/frontend/

FROM base-stage as dev-stage

# Start development server
CMD ["/bin/bash", "-c", "npm run serve"]

FROM base-stage as build-stage

# Compile build
RUN npm run build

FROM nginx as prod-stage

# Copy build to server container
COPY --from=build-stage /app/frontend/dist /app/

# Copy nginx configuration to server container
COPY nginx.conf /etc/nginx/nginx.conf
