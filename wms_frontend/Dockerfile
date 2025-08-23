FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/staticfiles /app/media

EXPOSE 8001

RUN echo 'from django.http import JsonResponse\nfrom django.urls import path\n\ndef health_check(request):\n    return JsonResponse({"status": "healthy"})\n\nurlpatterns = [path("health/", health_check, name="health")]' > health_urls.py

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "2", "--timeout", "60", "wms_frontend.wsgi:application"]