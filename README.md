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

**Development:**
```bash
chmod +x app_dev.sh
./app_dev.sh
```

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000/api
- Admin: http://localhost:8000/admin


### Development Management Commands

```bash
cd wms_api && python manage.py migrate --settings='wms_api.settings.development'
cd wms_api && python manage.py createsuperuser --settings='wms_api.settings.development'
cd wms_frontend && python manage.py migrate --settings='wms_frontend.settings.development'

cd wms_api && python manage.py update_instruments --settings='wms_api.settings.development'
cd wms_api && python manage.py update_lestypes --settings='wms_api.settings.development'
cd wms_api && python manage.py update_locaties --settings='wms_api.settings.development'
cd wms_api && python manage.py update_vakanties --settings='wms_api.settings.development'
```

### Environment Variables

Create `.env` files:

**`wms_api/.env`**:
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

**`wms_frontend/.env`**:
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

### Production Deployment Commands

```bash
chmod +x deploy.sh ssl-setup.sh
./deploy.sh
./ssl-setup.sh  # First time only
```

### Production Management Commands

```bash
docker compose exec wms_api python manage.py migrate --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py createsuperuser --settings='wms_api.settings.production'
docker compose exec wms_frontend python manage.py migrate --settings='wms_frontend.settings.production'

docker compose exec wms_api python manage.py collectstatic --noinput --settings='wms_api.settings.production'
docker compose exec wms_frontend python manage.py collectstatic --noinput --settings='wms_frontend.settings.production'

docker compose exec wms_api python manage.py update_instruments --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py update_lestypes --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py update_locaties --settings='wms_api.settings.production'
docker compose exec wms_api python manage.py update_vakanties --settings='wms_api.settings.production'
```

## Core Modules

- **activiteiten** - Cursus, Workshop, Project, Groep
- **agenda** - Posts, Events, Vakanties
- **knack** - Instrument, Locatie, Lestypes, Lestatief, Docent
- **muziekschool** - Over, Vacature, Contact, Header, Banner, Voorwaarde
- **stichting** - Overeenkomst, Sponsor, Anbi, Document
- **inbox** - Bericht, Proefles, Betalingsplichtige, Inschrijving
- **branding** - Assets, Design patterns

## API Endpoints

```
/api/activiteiten/    # Cursussen, Workshops, Projecten, Groepen
/api/agenda/          # Posts, Events, Vakanties
/api/knack/           # Instrumenten, Lestypes, Lestarieven, Locaties, Docenten
/api/muziekschool/    # Over, Contact, Vacatures, Headers, Banners, Voorwaarden
/api/stichting/       # Overeenkomsten, Sponsors, Anbi, Documents
/api/branding/        # Assets, Design patterns
/api/inbox/           # Berichten, Proeflessen, Betalingsplichtigen, Inschrijvingen
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
docker compose restart

docker compose logs wms_api
docker compose logs wms_frontend

docker compose down && docker compose up -d

docker compose run --rm certbot certificates
``` 