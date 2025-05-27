#!/bin/bash

black .

alembic upgrade head

uvicorn app.server.main:create_app --host 0.0.0.0 --port 8000 --reload --factory
