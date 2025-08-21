#!/bin/bash
# health-check.sh

PROJECT_DIR="/home/deploy/apps/WMS"
cd "$PROJECT_DIR"

# Load environment variables from .env file
if [ -f ".env" ]; then
    source .env
else
    echo "Error: .env file not found!"
    exit 1
fi

DOMAIN="$CERTBOT_DOMAIN"

if [ -z "$DOMAIN" ]; then
    echo "Error: CERTBOT_DOMAIN not set in .env file"
    exit 1
fi

echo "Health check for $DOMAIN at $(date)"

# Check if containers are running
echo "Checking container status..."
if ! docker compose ps | grep -q "Up"; then
    echo "⚠ Some containers are down! Restarting..."
    docker compose up -d
    sleep 30
else
    echo "✓ All containers are running"
fi

# Check individual container health
for service in wms_api wms_frontend nginx; do
    status=$(docker compose ps --filter "service=$service" --format "{{.State}}")
    if [[ "$status" == *"Up"* ]]; then
        echo "✓ $service: $status"
    else
        echo "✗ $service: $status"
        echo "Recent logs for $service:"
        docker compose logs --tail=10 "$service"
    fi
done

# Check SSL certificate expiry
CERT_PATH="/var/lib/docker/volumes/wms_certbot_conf/_data/live/$DOMAIN/cert.pem"

if [ -f "$CERT_PATH" ]; then
    echo "Checking SSL certificate for $DOMAIN..."
    if openssl x509 -checkend 604800 -noout -in "$CERT_PATH" 2>/dev/null; then
        echo "✓ SSL certificate is valid for more than 7 days"
        
        # Show certificate details
        expiry_date=$(openssl x509 -enddate -noout -in "$CERT_PATH" | cut -d= -f2)
        echo "  Certificate expires: $expiry_date"
    else
        echo "⚠ SSL certificate expires within 7 days or is invalid!"
        echo "  Run ssl-renew.sh to renew"
        
        # Try to renew automatically
        echo "Attempting automatic renewal..."
        docker compose run --rm certbot renew --quiet
        if [ $? -eq 0 ]; then
            echo "✓ Certificate renewed successfully"
            docker compose restart nginx
        else
            echo "✗ Certificate renewal failed"
        fi
    fi
else
    echo "⚠ SSL certificate not found at $CERT_PATH"
    echo "  Run ./ssl-setup.sh to create SSL certificates"
fi

# Test HTTP/HTTPS connectivity
echo "Testing connectivity..."

# Test HTTP
if curl -4 -I -s --connect-timeout 10 "http://$DOMAIN" | grep -q "HTTP"; then
    echo "✓ HTTP connection successful"
else
    echo "✗ HTTP connection failed"
fi

# Test HTTPS (if certificates exist)
if [ -f "$CERT_PATH" ]; then
    if curl -4 -I -s --connect-timeout 10 "https://$DOMAIN" | grep -q "HTTP"; then
        echo "✓ HTTPS connection successful"
    else
        echo "✗ HTTPS connection failed"
    fi
fi

# Check disk space
echo "Checking disk space..."
df_output=$(df -h / | tail -1)
disk_usage=$(echo $df_output | awk '{print $5}' | sed 's/%//')
if [ "$disk_usage" -gt 80 ]; then
    echo "⚠ Disk usage high: $disk_usage%"
    echo "Consider cleaning up with: docker system prune -a"
else
    echo "✓ Disk usage OK: $disk_usage%"
fi

# Check memory usage
echo "Checking memory usage..."
free -h

# Log the health check
echo "Health check completed at $(date)" >> /var/log/wms-health.log