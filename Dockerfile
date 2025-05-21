# Dockerfile

FROM python:3.11-slim

WORKDIR /home/app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SQLALCHEMY_DATABASE_URI=postgresql://saiful:saiful123@dse_postgres:5432/saas_dse_db

RUN chmod +x migrate.sh

# Run Alembic migrations then start FastAPI
CMD ./migrate.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
