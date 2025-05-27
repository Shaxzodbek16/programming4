# Kindergarten Management System

A comprehensive system for managing kindergarten operations, including kitchen inventory, meal tracking, and report
generation.

## Tech Stack

- Python
- PostgreSQL
- Redis
- Docker

## Prerequisites

Ensure the following are installed:

- Docker & Docker Compose
- Python 3.x
- Git

## Environment Setup

Create a `.env` file in the root directory with the following configuration:

```env
API_V1_STR=/api/v1
BASE_URL=http://localhost:8000

PROJECT_NAME=Kindergarden
PROJECT_DESCRIPTION='indergarden management system'
PROJECT_VERSION=0.0.1

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

EMAIL_PASSWORD='abcd efgh ijkl mnop'
EMAIL=example@gmail.com
SMTP_PORT=587
SMTP_SERVER=smtp.gmail.com

SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
REFRESH_TOKEN_EXPIRE_MINUTES=60
```

## Running the Application

To run the system:

```bash
docker-compose up --build -d
```

## Accessing the Application

Visit: [http://localhost:8000](http://localhost:8000)

## API Documentation

Access it here: [http://localhost:8000](http://localhost:8000)

## Notes

- Make sure the `.env` file is correctly configured before launching the containers.
- This system includes ingredient tracking, role-based access, and reporting functionalities for effective kindergarten
  food service management.

Enjoy using the Kindergarten Management System! 😊