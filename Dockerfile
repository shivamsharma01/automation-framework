# Stage 1: Build Angular App
FROM node:18 AS build-stage

WORKDIR /app

COPY ui-framework/package*.json ./
RUN npm install

COPY ui-framework/ ./
RUN npm run build --prod

# Stage 2: Setup Nginx and FastAPI
FROM python:3.11-slim AS production-stage

# Set up Nginx
RUN apt-get update && apt-get install -y nginx

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist/ui-framework /usr/share/nginx/html

RUN apt-get update && apt-get install -y chromium-driver wget nano

# Set up FastAPI
WORKDIR /app
COPY backend-server/ /app
RUN pip install --upgrade pip
RUN pip install numexpr numpy pandas python-dateutil pytz six tzdata pydantic  
RUN pip install uvicorn fastapi selenium fuzzywuzzy spacy scikit-learn python-Levenshtein
RUN pip install python-multipart webdriver_manager chromedriver_autoinstaller
RUN python -m spacy download en_core_web_md

ENV username="aalam.cheema@gmail.com"
ENV password="Asurasaurus1!"

RUN mkdir -p /app/files
RUN apt autoremove

# Expose ports
EXPOSE 80 8000

# Start both Nginx and FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
