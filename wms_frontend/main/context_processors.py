# main/context_processors.py
import requests
from django.conf import settings
from django.core.cache import cache

def branding_context(request):
    try:
        response_assets = requests.get(f"{settings.API_BASE_URL}branding/assets/")
        response_design = requests.get(f"{settings.API_BASE_URL}branding/design/")
        response_results = response_assets.json()['results']
        design_results = response_design.json()['results']

        assets = response_results[0] if response_assets.status_code == 200 and response_results else {}
        design = design_results[0] if response_design.status_code == 200 and design_results else {}

    except Exception:
        assets = {}
        design = {}

    return {
        "branding_assets": assets,
        "design_patterns": design,
    }

def contact_info(request):
    contact = cache.get('contact_info')
    if not contact:
        try:
            response = requests.get(f'{settings.API_BASE_URL}muziekschool/contact/')
            if response.status_code == 200:
                contact = response.json()['results'][0]
                cache.set('contact_info', contact, 3600)  # cache for 1h
            else:
                contact = None
        except requests.RequestException:
            contact = None
    return {'contact_info': contact}