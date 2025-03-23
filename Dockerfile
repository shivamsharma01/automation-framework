# Stage 1: Build Angular App
FROM node:18 AS build-stage

WORKDIR /app

# Install dependencies first (cached if unchanged)
COPY ui-framework/package*.json ./
RUN npm install

# Copy the rest of the frontend code and build
COPY ui-framework/ ./
RUN npm run build --prod

# Stage 2: Setup Nginx and FastAPI
FROM python:3.11-slim AS production-stage

# Install Nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy Nginx configuration
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy built Angular files from previous stage
COPY --from=build-stage /app/dist/ui-framework /usr/share/nginx/html

# Set up FastAPI backend
WORKDIR /app

# Install dependencies first to leverage caching
COPY backend-server/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend-server/ /app

# Additional dependencies
RUN pip install --no-cache-dir spacy rapidfuzz
RUN python -m spacy download en_core_web_md

# Create necessary directories
RUN mkdir -p /app/files

# Expose ports
EXPOSE 80 8000

# Entrypoint script to start both services
COPY backend-server/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
