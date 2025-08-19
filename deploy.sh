#!/bin/bash
# deploy.sh

echo "Starting deployment..."

# Pull latest code
git pull origin main

# Build and restart containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run migrations
docker-compose exec wms_api python manage.py migrate
docker-compose exec wms_frontend python manage.py migrate

# Collect static files
docker-compose exec wms_api python manage.py collectstatic --noinput
docker-compose exec wms_frontend python manage.py collectstatic --noinput

echo "Deployment completed!"

chmod +x deploy.sh

# Temporarily modify nginx.conf to only serve HTTP for certificate generation
docker-compose up -d nginx

# Get SSL certificates
docker-compose run --rm certbot

# Then update nginx.conf with SSL configuration and restart
docker-compose restart nginx

# Add to crontab
crontab -e

# Add this line (runs twice daily)
0 12 * * * /usr/local/bin/docker-compose -f /home/deploy/apps/docker-compose.yml run --rm certbot renew && /usr/local/bin/docker-compose -f /home/deploy/apps/docker-compose.yml restart nginx