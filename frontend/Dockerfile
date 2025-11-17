FROM node:22 AS build

WORKDIR /app

COPY stud_assistant/package*.json ./

RUN npm install

COPY stud_assistant/ .

RUN npm run build

# Serve stage
FROM nginx:1.25
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

