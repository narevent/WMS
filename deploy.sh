#!/bin/bash
# deploy.sh

REPO_URL="https://github.com/narevent/WMS.git"
PROJECT_DIR="/home/deploy/apps/WMS"
BRANCH="main"

echo "Starting deployment..."

if ! groups $USER | grep &>/dev/null '\bdocker\b'; then
    echo "Warning: Current user is not in the docker group."
    echo "You may need to run this script with sudo or add user to docker group."
fi

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
docker compose down

echo "Pruning unused Docker resources..."
docker system prune -f

echo "Building containers..."
docker compose build --no-cache

echo "Starting containers..."
docker compose up -d

echo "Waiting for containers to start..."
sleep 10

echo "Checking container health..."
docker compose ps

echo "Running migrations..."
docker compose exec -T wms_api python manage.py migrate --noinput --settings=wms_api.settings.production
docker compose exec -T wms_frontend python manage.py migrate --noinput --settings=wms_api.settings.production

echo "Collecting static files..."
docker compose exec -T wms_api python manage.py collectstatic --noinput --settings=wms_api.settings.production
docker compose exec -T wms_frontend python manage.py collectstatic --noinput --settings=wms_api.settings.production

echo "Testing health endpoints..."
sleep 10
docker compose exec nginx curl -f http://wms.trackisolator.com/api/health/ || echo "WARNING: API health check failed"
docker compose exec nginx curl -f http://wms.trackisolator.com/health/ || echo "WARNING: Frontend health check failed"

echo "Deployment completed!"
echo ""
echo "Note: If this is your first deployment, run './ssl-setup.sh' to configure SSL certificates."