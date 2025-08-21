FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

RUN python manage.py collectstatic

EXPOSE 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "wms_frontend.wsgi:application"]