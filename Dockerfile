FROM python:3.11-alpine

WORKDIR /app

COPY keepalive.py .
COPY urls.txt* ./

RUN chmod +x keepalive.py

CMD ["python3", "keepalive.py"]
