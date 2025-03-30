# Use Node.js for building Vue
FROM node:18 AS build
WORKDIR /app

# Create .env file from build args
ARG VUE_APP_GOOGLE_MAPS_API_KEY
ARG VUE_APP_WEATHER_API_KEY
ARG VUE_APP_API_URL

ENV VUE_APP_GOOGLE_MAPS_API_KEY=${VUE_APP_GOOGLE_MAPS_API_KEY}
ENV VUE_APP_WEATHER_API_KEY=${VUE_APP_WEATHER_API_KEY}
ENV VUE_APP_API_URL=${VUE_APP_API_URL}

COPY package.json package-lock.json ./
RUN npm install

# Copy public directory first to ensure images are available
COPY public ./public

# Copy the rest of the application
COPY . .
RUN npm run build

# Use Nginx to serve Vue app
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/public/images /usr/share/nginx/html/images
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
