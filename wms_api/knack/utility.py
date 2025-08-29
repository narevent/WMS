# knack/management/commands/utility.py
import json
import os
import pickle
from datetime import datetime
from typing import Any, Dict, List
import requests
import base64
from django.conf import settings

HEADERS = {'Content-Type': 'application/json'}
URL_BASE = 'https://api.knack.com/v1/'
URL_TOKEN = URL_BASE + 'applications/%s/session'
URL_POST = URL_BASE + 'pages/scene_%d/views/view_%d/records'
URL_RECORDS = URL_POST + '?format=raw&rows_per_page=1000&page=%d'

END_POINTS = {
    "Instruments": {'get': (148, 228)},
    "Lestypes": {'get': (148, 229)},
    "Zalen": {'get': (148, 230)},
}

def get_header(token: str) -> Dict[str, str]:
    header = HEADERS.copy()
    header.update({"X-Knack-Application-Id": settings.KNACK_ID})
    header.update({"Authorization": token})
    return header

def get_token() -> str:
    payload = {'email': settings.KNACK_MAIL, 'password': settings.KNACK_PASS}
    url = URL_TOKEN % settings.KNACK_ID
    r = requests.post(url, data=json.dumps(payload), headers=HEADERS)
    data = json.loads(r.text)['session']['user']
    return data['token']

def get_data(token: str, scene_id: int, view_id: int, page: int = 1) \
        -> Dict[str, Any]:
    HEADERS.update({'X-Knack-Application-Id': settings.KNACK_ID})
    HEADERS.update({'Authorization': token})
    url = URL_RECORDS % (scene_id, view_id, page)
    r = requests.get(url, headers=HEADERS)
    return json.loads(r.text)

def get_records(name: str) -> List[Any]:
    file_path = os.path.join(settings.CACHE_DIR, f"{name.lower()}.pickle")
    if os.path.isfile(file_path):
        now = datetime.now().timestamp()
        mtime = os.path.getmtime(file_path)
        age = (now - mtime) / 3600
        if age > 3:
            os.remove(file_path)
        else:
            with open(file_path, 'rb') as f:
                return pickle.load(f)

    scene_id, view_id = END_POINTS[name]['get']
    token = get_token()

    records, page = [], 1
    while True:
        data_dict = get_data(token, scene_id, view_id, page)
        total_pages = data_dict['total_pages']
        records += data_dict['records']
        if page >= total_pages:
            break
        else:
            page += 1

    with open(file_path, 'wb') as f:
        pickle.dump(records, f)

    return records

def get_django_auth_headers():
    credentials = base64.b64encode(f'{settings.DJANGO_USERNAME}:{settings.DJANGO_PASSWORD}'.encode()).decode()
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}'
    }

def post_api_data(endpoint, data):
    try:
        headers = get_django_auth_headers()
        response = requests.post(f"{settings.API_BASE_URL}{endpoint}/", json=data, headers=headers)
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def get_or_create_api_data(endpoint, data):
    try:
        headers = get_django_auth_headers()
        print(f"Attempting to GET resource from {endpoint} with data: {data}...")
        get_response = requests.get(f"{settings.API_BASE_URL}{endpoint}/", params=data, headers=headers)

        if get_response.status_code == 200:
            print("Resource found. Returning existing resource.")
            return get_response
        elif get_response.status_code == 404:
            print("Resource not found (404). Proceeding to create it with POST request...")
            post_response = post_api_data(f"{settings.API_BASE_URL}{endpoint}/", json=data)
            post_response.raise_for_status()
            print("Resource successfully created.")
            return post_response
        else:
            print(f"Unexpected status code for GET request: {get_response.status_code}")
            get_response.raise_for_status()
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None