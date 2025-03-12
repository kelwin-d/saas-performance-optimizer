FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install fastapi sqlalchemy cachetools

CMD ["uvicorn", "performance_optimizer:app", "--host", "0.0.0.0", "--port", "8000"]
