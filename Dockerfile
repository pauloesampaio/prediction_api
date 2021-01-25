FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app/app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ /app/app/
