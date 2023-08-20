# syntax=docker/dockerfile:1
   
FROM node:18-alpine

WORKDIR /frontEnd

COPY . .

RUN npm install

CMD ["npm", "run", "dev"]
