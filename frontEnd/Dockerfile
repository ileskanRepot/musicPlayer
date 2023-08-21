# syntax=docker/dockerfile:1
   
FROM node:18-alpine as build

WORKDIR /frontEnd

COPY tsconfig.node.json package-lock.json package.json  ./
RUN npm ci

COPY tsconfig.json ./
COPY src ./scr
COPY public ./public

RUN npm run build

FROM nginx AS run

COPY --from=build /frontEnd/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 5173
