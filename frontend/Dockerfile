# build-stage
FROM node:lts as build-stage

WORKDIR /app/frontend/

COPY package*.json /app/frontend/

RUN npm install

COPY ./ /app/frontend/

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/frontend/dist /app/

COPY nginx.conf /etc/nginx/nginx.conf
