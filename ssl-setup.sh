#!/bin/bash
# ssl-setup.sh - Run this ONCE after initial deployment

PROJECT_DIR="/home/deploy/apps/WMS"

# Load environment variables from .env file
if [ -f ".env" ]; then
    source .env
    echo "Loaded environment variables from .env"
else
    echo "Error: .env file not found!"
    exit 1
fi

# Use variables from .env file
DOMAIN="$CERTBOT_DOMAIN"
EMAIL="$CERTBOT_EMAIL"

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Error: CERTBOT_DOMAIN and CERTBOT_EMAIL must be set in .env file"
    exit 1
fi

echo "Setting up SSL certificates for $DOMAIN..."
echo "Using email: $EMAIL"

cd "$PROJECT_DIR"

# Check if domain resolves to this server
echo "Checking domain resolution..."
SERVER_IP=$(curl -4 -s ifconfig.me)
DOMAIN_IP=$(dig +short $DOMAIN)

echo "Server IP: $SERVER_IP"
echo "Domain IP: $DOMAIN_IP"

if [ "$SERVER_IP" != "$DOMAIN_IP" ]; then
    echo "WARNING: Domain $DOMAIN does not point to this server ($SERVER_IP)"
    echo "Make sure your DNS A record points $DOMAIN to $SERVER_IP"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Ensure all services are stopped
echo "Stopping all services..."
docker compose down

# Start only nginx in HTTP-only mode first
echo "Creating temporary nginx config for certificate challenge..."

# Backup original nginx config if it exists
if [ -f "nginx/nginx.conf" ]; then
    cp nginx/nginx.conf nginx/nginx.conf.backup
fi

# Create a simple HTTP-only nginx config for certificate challenge
mkdir -p nginx
cat > nginx/nginx.conf.temp << EOF
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name $DOMAIN;
        
        # Let's Encrypt challenge location
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        # Redirect all other traffic to HTTPS (after we get certificates)
        location / {
            return 301 https://\$server_name\$request_uri;
        }
    }
}
EOF

# Use temporary config
cp nginx/nginx.conf.temp nginx/nginx.conf

# Start nginx with temporary config
echo "Starting nginx for certificate challenge..."
docker compose up -d nginx

# Wait for nginx to start
sleep 15

# Check if nginx is accessible
echo "Testing nginx accessibility..."
if curl -I -s --connect-timeout 10 http://$DOMAIN/.well-known/acme-challenge/test | grep -q "404\|200"; then
    echo "✓ Nginx is accessible on port 80"
else
    echo "✗ Cannot reach nginx on port 80. Check firewall and DNS."
    echo "Debug information:"
    docker compose logs nginx
    exit 1
fi

# Request SSL certificate with more verbose output
echo "Requesting SSL certificate from Let's Encrypt..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --verbose \
    --dry-run \
    -d $DOMAIN

# If dry run succeeds, do the real request
if [ $? -eq 0 ]; then
    echo "Dry run successful! Now requesting real certificate..."
    docker compose run --rm certbot certonly \
        --webroot \
        --webroot-path=/var/www/certbot \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN
        
    if [ $? -eq 0 ]; then
        echo "✓ SSL certificate obtained successfully!"
        
        # Restore original nginx config or create production config
        if [ -f "nginx/nginx.conf.backup" ]; then
            mv nginx/nginx.conf.backup nginx/nginx.conf
            echo "Restored original nginx configuration"
        else
            echo "Creating production nginx configuration with SSL..."
            cat > nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=login:10m rate=10r/m;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    upstream wms_api {
        server wms_api:8000;
    }
    
    upstream wms_frontend {
        server wms_frontend:8001;
    }
    
    # HTTP redirect to HTTPS
    server {
        listen 80;
        server_name $DOMAIN;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 301 https://\$server_name\$request_uri;
        }
    }
    
    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name $DOMAIN;
        
        ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
        
        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # API routes
        location /api/ {
            proxy_pass http://wms_api;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Static files for API
        location /static/api/ {
            alias /var/www/wms_api/static/;
        }
        
        location /media/api/ {
            alias /var/www/wms_api/media/;
        }
        
        # Frontend routes
        location / {
            proxy_pass http://wms_frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Static files for frontend
        location /static/ {
            alias /var/www/wms_frontend/static/;
        }
        
        location /media/ {
            alias /var/www/wms_frontend/media/;
        }
    }
}
EOF
        fi
        
        # Restart all services with SSL config
        echo "Restarting all services with SSL configuration..."
        docker compose down
        docker compose up -d
        
        # Wait for services to start
        sleep 30
        
        # Test HTTPS
        echo "Testing HTTPS connection..."
        if curl -I -s --connect-timeout 10 https://$DOMAIN | grep -q "200\|301\|302"; then
            echo "✓ HTTPS is working!"
        else
            echo "⚠ HTTPS test failed, but certificates are installed"
        fi
        
        # Set up auto-renewal
        echo "Setting up SSL certificate auto-renewal..."
        
        # Create renewal script with correct path
        cat > ssl-renew.sh << EOF
#!/bin/bash
cd $PROJECT_DIR
docker compose run --rm certbot renew --quiet
if [ \$? -eq 0 ]; then
    docker compose restart nginx
fi
EOF
        
        chmod +x ssl-renew.sh
        
        # Add to crontab (runs twice daily)
        (crontab -l 2>/dev/null; echo "0 12,0 * * * $PROJECT_DIR/ssl-renew.sh >> /var/log/ssl-renew.log 2>&1") | crontab -
        
        echo "✅ SSL setup completed successfully!"
        echo "Certificate auto-renewal configured in crontab"
        echo ""
        echo "You can check certificate status with:"
        echo "docker compose run --rm certbot certificates"
        
    else
        echo "❌ SSL certificate request failed!"
        echo "Check the logs above for details"
        
        # Restore original config
        if [ -f "nginx/nginx.conf.backup" ]; then
            mv nginx/nginx.conf.backup nginx/nginx.conf
        fi
        exit 1
    fi
else
    echo "❌ Dry run failed! Check domain configuration and try again"
    echo "Make sure:"
    echo "1. Domain points to this server"
    echo "2. Port 80 is open in firewall"
    echo "3. No other service is using port 80"
    
    # Show nginx logs for debugging
    echo ""
    echo "Nginx logs:"
    docker compose logs nginx
    
    exit 1
fi

# Cleanup temp files
rm -f nginx/nginx.conf.temp