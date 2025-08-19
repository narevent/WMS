# api_client/views.py
import requests
from django.conf import settings
from django.urls import reverse

def get_api_data(endpoint):
    try:
        response = requests.get(f"{settings.API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            json_response = response.json()
            if 'results' in list(json_response.keys()):
                return json_response['results'] # list view
            else:
                return json_response # detail view
        return []
    except requests.RequestException:
        return []

def post_api_data(endpoint, data):
    try:
        response = requests.post(f"{settings.API_BASE_URL}{endpoint}", json=data)
        return response
    except requests.RequestException:
        return None
    
def normalize_items(items, url_name):
    return [
        {
            'url': reverse(url_name, args=[item['id']]),
            'image': item.get('image'),
            'title': item.get('naam'),
            'description': item.get('beschrijving'),
            'price': item.get('prijs'),
        }
        for item in items
    ]

def normalize_item(item):
    return {
            'image': item.get('image'),
            'title': item.get('naam'),
            'description': item.get('beschrijving'),
            'price': item.get('prijs'),
        }

