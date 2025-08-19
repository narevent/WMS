#!/bin/bash
# deploy.sh

REPO_URL="https://github.com/narevent/WMS.git"
PROJECT_DIR="/home/deploy/apps"
BRANCH="main"

echo "Starting deployment..."

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

if [ -d ".git" ]; then
    echo "Repository exists, pulling latest changes..."
    git fetch origin
    git reset --hard origin/$BRANCH
else
    echo "Initial setup: Cloning repository..."
    git clone "$REPO_URL" .
    git checkout "$BRANCH"
fi

git checkout "$BRANCH"
echo "Current commit: $(git rev-parse HEAD)"

echo "Stopping existing containers..."
docker-compose down

echo "Building containers..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up -d

echo "Waiting for containers to start..."
sleep 30

echo "Running migrations..."
docker-compose exec -T wms_api python manage.py migrate
docker-compose exec -T wms_frontend python manage.py migrate

echo "Collecting static files..."
docker-compose exec -T wms_api python manage.py collectstatic --noinput
docker-compose exec -T wms_frontend python manage.py collectstatic --noinput

echo "Deployment completed successfully!"

setup_ssl() {
    echo "Setting up SSL certificates..."
    docker-compose up -d nginx
    docker-compose run --rm certbot
    docker-compose restart nginx
    echo "SSL setup completed!"
}

# Uncomment the line below for initial setup with SSL
# setup_ssl

# Note: Add SSL certificate renewal to crontab manually:
# crontab -e
# Add this line (runs twice daily):
# 0 12 * * * /usr/local/bin/docker-compose -f /home/deploy/apps/docker-compose.yml run --rm certbot renew && /usr/local/bin/docker-compose -f /home/deploy/apps/docker-compose.yml restart nginx