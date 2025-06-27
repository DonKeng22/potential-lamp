# Dockerfile for the React Frontend

# Use a Node.js base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app/frontend/web

# Copy package.json and package-lock.json (if exists) to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .
# Build the React app for production
RUN npm run build

# Use a lightweight web server to serve the static files
FROM nginx:alpine
COPY --from=0 /app/frontend/web/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
