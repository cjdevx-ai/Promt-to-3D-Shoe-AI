# Stage 1: Build the React application
FROM node:18-slim AS build

WORKDIR /app

# Accept the API URL as a build argument
ARG VITE_API_URL
# Set it as an environment variable for Vite
ENV VITE_API_URL=$VITE_API_URL

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (using legacy-peer-deps to avoid the Three.js conflict)
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . .

# Build the application
# Note: In production, you would set VITE_API_URL during the build process
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:stable-alpine

# Copy the build output to the Nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a custom Nginx configuration if needed (optional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (GCP Cloud Run will map this)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
