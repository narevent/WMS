#!/bin/bash
# ssl-setup.sh - Run this ONCE after initial deployment

PROJECT_DIR="/home/deploy/apps/WMS"  # Adjust to match your deploy script
DOMAIN="wms.trackisolator.com"  # Replace with your actual domain

echo "Setting up SSL certificates for $DOMAIN..."

cd "$PROJECT_DIR"

# Ensure nginx is configured for HTTP first (for certificate challenge)
echo "Starting nginx in HTTP-only mode for certificate generation..."
docker-compose up -d nginx

# Wait for nginx to start
sleep 10

# Request SSL certificate
echo "Requesting SSL certificate from Let's Encrypt..."
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@$DOMAIN \
  --agree-tos \
  --no-eff-email \
  -d $DOMAIN

if [ $? -eq 0 ]; then
    echo "SSL certificate obtained successfully!"
    
    # Now update nginx config to use SSL and restart
    echo "Restarting nginx with SSL configuration..."
    docker-compose restart nginx
    
    # Set up auto-renewal cron job
    echo "Setting up SSL certificate auto-renewal..."
    
    # Create renewal script
    cat > ssl-renew.sh << 'EOF'
#!/bin/bash
cd /home/deploy/apps
docker-compose run --rm certbot renew --quiet
if [ $? -eq 0 ]; then
    docker-compose restart nginx
fi
EOF
    
    chmod +x ssl-renew.sh
    
    # Add to crontab (runs twice daily)
    (crontab -l 2>/dev/null; echo "0 12,0 * * * /home/deploy/apps/ssl-renew.sh >> /var/log/ssl-renew.log 2>&1") | crontab -
    
    echo "SSL setup completed! Auto-renewal configured."
    echo "Check certificate status with: docker-compose run --rm certbot certificates"
else
    echo "SSL certificate request failed. Check your domain configuration."
    exit 1
fi