FROM python:3.10-slim

WORKDIR /app

COPY ./platform/backend/requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./platform/backend /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
