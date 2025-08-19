#!/bin/bash
# health-check.sh

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "Some containers are down! Restarting..."
    docker-compose up -d
fi

# Check SSL certificate expiry
if openssl x509 -checkend 604800 -noout -in /var/lib/docker/volumes/apps_certbot_conf/_data/live/trackisolator.com/cert.pem; then
    echo "SSL certificate is valid for more than 7 days"
else
    echo "SSL certificate expires soon!"
fi