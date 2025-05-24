#!/bin/bash

black .

sleep 3

alembic revision --autogenerate -m "migrations"

sleep 3

alembic upgrade head

sleep 3

uvicorn app.server.main:create_app --host 0.0.0.0 --port 8000 --reload --factory
