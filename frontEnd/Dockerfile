# syntax=docker/dockerfile:1
   
FROM node:latest as build

WORKDIR /frontEnd

COPY tsconfig.node.json package-lock.json package.json  ./
RUN npm ci \
	&& npm install typescript -g


COPY tsconfig.json ./
COPY src ./src
COPY index.html ./
COPY public ./public

RUN ls src

RUN npm run build

FROM nginx AS run

COPY --from=build /frontEnd/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 5173
