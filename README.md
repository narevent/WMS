# WMS - Wereldmuziekschool

Django-based music school management system with separate API and frontend applications.

**Architecture:**
- `wms_api` - Django REST API backend
- `wms_frontend` - Django template-based frontend
- `nginx` - Reverse proxy with SSL termination
- `certbot` - Automated SSL certificate management

## Development Setup

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (for production)

### Quick Start

**If you don't have the code yet:**
```bash
git clone https://github.com/narevent/WMS && cd WMS
```

**Development (Native Python):**
```bash
chmod +x run_dev.sh
./run_dev.sh
```

**Development (Docker):**
```bash
docker compose up wms_api wms_frontend
```

Access:
- Frontend: http://localhost:3000
- API/Admin: http://localhost:8000/admin

### Development Management Commands

```bash
# Native Python
cd wms_api && python manage.py migrate --settings='wms_api.settings.development'
cd wms_api && python manage.py createsuperuser --settings='wms_api.settings.development'
cd wms_frontend && python manage.py migrate --settings='wms_frontend.settings.development'

# Docker (development settings)
docker compose exec wms_api python manage.py migrate --settings='wms_api.settings.development'
docker compose exec wms_api python manage.py createsuperuser --settings='wms_api.settings.development'
docker compose exec wms_frontend python manage.py migrate --settings='wms_frontend.settings.development'
```

### Environment Variables (Development)

Create `.env` files for both development and production:

**`wms_api/.env`** (required even for development):
```env
# Knack API Integration
KNACK_MAIL=your-knack-email@domain.com
KNACK_PASS=your-knack-password
KNACK_ID=your-knack-application-id

# Cache and Data
CACHE_DIR=./cache

# Django Admin API Access
DJANGO_USERNAME=your-django-username
DJANGO_PASSWORD=your-django-password

# Development can use defaults for these:
DJANGO_SECRET_KEY=django-insecure-change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
API_BASE_URL=http://localhost:8000/api/
```

**`wms_frontend/.env`** (required even for development):
```env
# Django Admin API Access
DJANGO_USERNAME=your-django-username
DJANGO_PASSWORD=your-django-password

# Development can use defaults for these:
DJANGO_SECRET_KEY=django-insecure-change-me-frontend
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
API_BASE_URL=http://localhost:8000/api/
```

## Production Deployment

### Environment Configuration

**Root `.env`** (for Docker Compose and SSL):
```env
CERTBOT_EMAIL=admin@yourdomain.com
CERTBOT_DOMAIN=yourdomain.com
```

**`wms_api/.env`** (API production settings):
```env
# Knack API Integration (Required)
KNACK_MAIL=your-knack-email@domain.com
KNACK_PASS=your-knack-password
KNACK_ID=your-knack-application-id

# Cache and Data
CACHE_DIR=/app/cache

# Django Admin API Access (Required)
DJANGO_USERNAME=your-django-username
DJANGO_PASSWORD=your-django-password

# Production Settings (Required)
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
API_BASE_URL=https://yourdomain.com/api/
```

**`wms_frontend/.env`** (Frontend production settings):
```env
# Django Admin API Access (Required)
DJANGO_USERNAME=your-django-username
DJANGO_PASSWORD=your-django-password

# Production Settings (Required)
DJANGO_SECRET_KEY=your-different-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
API_BASE_URL=https://yourdomain.com/api/
```

### Production Deployment Commands

```bash
# Create environment files (see above)
chmod +x deploy.sh ssl-setup.sh
./deploy.sh
./ssl-setup.sh  # First time only
```

### Production Management Commands

```bash
# Database operations (production settings)
docker compose exec wms_api python manage.py migrate --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py createsuperuser --settings='wms_api.settings.production'
docker compose exec wms_frontend python manage.py migrate --settings='wms_frontend.settings.production'

# Static files
docker compose exec wms_api python manage.py collectstatic --noinput --settings='wms_api.settings.production'
docker compose exec wms_frontend python manage.py collectstatic --noinput --settings='wms_frontend.settings.production'

# Data updates
docker compose exec wms_api python manage.py update_instruments --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py update_vakanties --settings='wms_api.settings.production'
```

## Core Modules

- **activiteiten** - Courses and workshops
- **agenda** - Events and posts  
- **knack** - Instruments, locations, lesson types
- **muziekschool** - School info, jobs, contacts
- **stichting** - Foundation information
- **branding** - Design patterns
- **inbox** - Registrations and inquiries

## API Endpoints

```
/api/activiteiten/    # Courses, workshops
/api/agenda/          # Events, posts
/api/knack/           # Instruments, teachers, lesson types
/api/muziekschool/    # School data, jobs
/api/stichting/       # Foundation info
/api/branding/        # Design patterns
/api/inbox/           # Registrations
```

All endpoints support filtering, search, ordering, and pagination.

## Operations

```bash
# Deploy updates
./deploy.sh

# Backup
./backup.sh

# SSL renewal (automated via cron)
./ssl-renew.sh

# Logs
docker compose logs [service]

# Status
docker compose ps
```

## Tech Stack

- **Backend:** Django 4.2, DRF 3.16, TinyMCE, Pillow
- **Frontend:** Django templates, TailwindCSS
- **Infrastructure:** Docker, Nginx, Let's Encrypt, SQLite
- **Features:** Rich text editing, file management, responsive design

## Health Checks

- API: `/api/health/`
- Frontend: `/health/`

Both return JSON status responses for monitoring.

## Troubleshooting

```bash
# Restart services
docker compose restart

# View logs
docker compose logs wms_api
docker compose logs wms_frontend

# Reset containers
docker compose down && docker compose up -d

# SSL issues
docker compose run --rm certbot certificates
``` 