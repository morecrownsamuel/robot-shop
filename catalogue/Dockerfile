FROM node:22-bookworm-slim

EXPOSE 8080

WORKDIR /opt/server

COPY package.json package-lock.json ./
RUN npm ci

COPY server.js tracing.js ./

CMD ["node", "server.js"]
