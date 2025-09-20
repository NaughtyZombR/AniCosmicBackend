#!/bin/bash

cd app || exit
alembic upgrade head
if [ "$1" = "--development" ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
  gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --timeout 300
fi