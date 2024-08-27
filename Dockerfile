# Stage 1: Build Angular App
FROM node:18 AS build-stage

WORKDIR /app

COPY ui-framework/package*.json ./
RUN npm install

COPY ui-framework/ ./
RUN npm run build --prod

# Stage 2: Setup Nginx and FastAPI
FROM python:3.11-slim AS production-stage

RUN apt-get update && apt-get install -y nginx

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist/ui-framework /usr/share/nginx/html

RUN apt-get update && apt-get install -y chromium-driver

WORKDIR /app
COPY backend-server/ /app
RUN pip install --upgrade pip
RUN pip install numexpr numpy pandas python-dateutil pytz six tzdata pydantic python-multipart tinydb
RUN pip install uvicorn fastapi fuzzywuzzy spacy scikit-learn python-Levenshtein together
RUN pip install selenium webdriver_manager chromedriver_autoinstaller
RUN python -m spacy download en_core_web_md

ENV username="aalam.cheema@gmail.com"
ENV password="Asurasaurus1!"
ENV together_api_key="03489e7ac45d4902acc2a923b7cb542971ee3d1c4657f3a9fb29b9f84996b8f7"

RUN mkdir -p /app/files
RUN apt autoremove

# Expose ports
EXPOSE 80 8000

# Start both Nginx and FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
