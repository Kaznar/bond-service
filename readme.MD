# bond-service Project

## Overview
The `bond-service` project is a Django-based application that allows users to manage and analyze their bond investments. This project utilizes Docker for containerization, PostgreSQL for the database, and Redis for caching.

## Prerequisites
Before you begin, ensure you have the following installed on your local machine:
- Docker
- Docker Compose

## Installation

1. **Clone the repository:**
   ```git clone https://github.com/Kaznar/bond-service.git```
   ```cd bond-service```

2. **Build and run the Docker containers:**
  ```docker compose up --build```

## Using Debug Mode
To run Django outside the container using a virtual environment for debugging, follow these steps:
For using debug mode you need run django out container in venv.
1. ```docker compose -f docker-compose.debug.yaml```
2. ```python3.12 -m venv venv```
3. ```. venv/bin/activate```
4. ```pip install -r requirements.txt```
5. Run Django in the virtual environment: You can now run Django commands in the virtual environment for debugging purposes.