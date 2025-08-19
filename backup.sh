#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/deploy/backups"

mkdir -p $BACKUP_DIR

# Backup databases
docker-compose exec wms_api python manage.py dumpdata > $BACKUP_DIR/wms_api_$DATE.json
docker-compose exec wms_frontend python manage.py dumpdata > $BACKUP_DIR/wms_frontend_$DATE.json

# Copy SQLite files
docker cp wms_api:/app/data/db.sqlite3 $BACKUP_DIR/wms_api_db_$DATE.sqlite3
docker cp wms_frontend:/app/data/db.sqlite3 $BACKUP_DIR/wms_frontend_db_$DATE.sqlite3

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.json" -mtime +7 -delete
find $BACKUP_DIR -name "*.sqlite3" -mtime +7 -delete