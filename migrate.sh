#!/bin/bash

echo "Running Alembic migrations..."

alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Alembic migration failed!"
    exit 1
fi

echo "Migrations applied successfully."
