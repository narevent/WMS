#!/bin/bash
# debug-502.sh - Script to diagnose 502 Bad Gateway issues

echo "=== Docker Container Status ==="
docker ps -a

echo ""
echo "=== Container Logs (Last 50 lines) ==="
echo "--- WMS API Logs ---"
docker logs --tail=50 wms_api

echo ""
echo "--- WMS Frontend Logs ---"
docker logs --tail=50 wms_frontend

echo ""
echo "--- Nginx Logs ---"
docker logs --tail=50 nginx

echo ""
echo "=== Network Connectivity Tests ==="
echo "Testing API container connectivity..."
docker exec nginx curl -f http://wms_api:8000/health/ || echo "API health check failed"

echo "Testing Frontend container connectivity..."
docker exec nginx curl -f http://wms_frontend:8001/health/ || echo "Frontend health check failed"

echo ""
echo "=== Port Listening Status ==="
echo "Checking if applications are listening on correct ports..."
docker exec wms_api netstat -tlnp | grep :8000 || echo "API not listening on port 8000"
docker exec wms_frontend netstat -tlnp | grep :8001 || echo "Frontend not listening on port 8001"

echo ""
echo "=== Django Application Status ==="
echo "Checking Django apps directly..."
docker exec wms_api python manage.py check || echo "API Django check failed"
docker exec wms_frontend python manage.py check || echo "Frontend Django check failed"