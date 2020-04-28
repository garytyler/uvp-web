# build-stage
FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

# RUN bash -c "if [ $ENVIRONMENT == 'development' ] ; then npm run serve ; else npm run build ; fi"

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /app

COPY nginx.conf /etc/nginx/nginx.conf
