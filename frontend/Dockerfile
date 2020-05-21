# build-stage
# FROM node:lts-alpine as build-stage
FROM node:lts as build-stage

WORKDIR /app

COPY package*.json /app/

# RUN npm install -g yarn
RUN npm install
# RUN yarn

COPY ./ /app/

# RUN bash -c "if [ $ENVIRONMENT == 'development' ] ; then npm run serve ; else npm run build ; fi"

RUN npm run build
# RUN yarn run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /app

COPY nginx.conf /etc/nginx/nginx.conf
