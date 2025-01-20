FROM node:22.13-alpine AS build

WORKDIR /app

# Copy the package.json and package-lock.json to take advantage of Docker caching
COPY package*.json ./

RUN npm config set legacy-peer-deps true && npm install && npm install ajv@latest ajv-keywords@latest

COPY . .

EXPOSE 3000

CMD ["npm", "start"]