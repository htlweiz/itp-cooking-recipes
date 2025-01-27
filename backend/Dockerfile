FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "python db/db.py && uvicorn main:app --host 0.0.0.0 --port 8002 --ssl-keyfile key.pem --ssl-certfile cert.pem"]
