
# Automation Framework

This repository contains a Docker-based automation framework. The framework is built using Docker, and this README provides instructions on how to build, push, pull, and run the Docker container for the framework.

## Prerequisites

- Docker installed on your machine.
- Docker Hub account for pushing and pulling images.

## Docker Commands

### 1. Build Docker Image

To build the Docker image, use the following command:

```bash
docker build -t shivamshivam01/aib:automation-framework .
```

### 2. Push Docker Image

After building the image, push it to Docker Hub using:

```bash
docker push shivamshivam01/aib:automation-framework
```

### 3. Pull Docker Image

To pull the Docker image from Docker Hub, use:

```bash
docker pull shivamshivam01/aib:automation-framework
```

### 4. Run Docker Container

Run the Docker container with the following command:

```bash
docker run -d -p 80:80 -p 8000:8000 shivamshivam01/aib:automation-framework
```

This command will run the container in detached mode and map port `80` and `8000` on your local machine to the same ports inside the container.


### 5. Start Application

To start the application, execute the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'
```

This command runs the application using Uvicorn on port `8000` and starts Nginx in the foreground.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
