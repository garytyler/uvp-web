FROM node:14-buster as node
FROM nginx:stable-alpine as nginx

FROM node as install-playwright-deps-stage

# Install browser dependencies for testing with playwright
# See: https://github.com/microsoft/playwright/blob/master/docs/docker/Dockerfile.bionic
# WebKit dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libnotify4 \
    libxslt1.1 \
    libevent-2.1-6 \
    libgles2 \
    libvpx5 \
    libxcomposite1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libepoxy0 \
    libgtk-3-0 \
    libharfbuzz-icu0

# gstreamer and plugins to support video playback in WebKit.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav

# Chromium dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libxtst6

# Firefox dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-glib-1-2 \
    libxt6

FROM install-playwright-deps-stage as install-stage

# Create target directory
RUN mkdir --parents /srv/app/frontend

# Set workdir to service destination
WORKDIR /srv/app/frontend

COPY package.json yarn.lock ./

# RUN npm install
RUN yarn config set yarn-offline-mirror ~/packages-cache
RUN yarn install

FROM install-stage as dev-stage

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
