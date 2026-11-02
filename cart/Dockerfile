FROM node:22-bookworm-slim

WORKDIR /opt/server

COPY package*.json ./

RUN npm ci --omit=dev

COPY server.js ./

EXPOSE 8080

CMD ["node", "server.js"]