# main/views.py
from django.shortcuts import render
from django.contrib import messages
from api_client.views import get_api_data, post_api_data

def custom_page_not_found_view(request, exception):
    return render(request, "main/404.html", status=404)

def custom_server_error_view(request):
    return render(request, "main/500.html", status=500)

def get_banners(banner_type='nieuws'):
    banners = get_api_data('muziekschool/banners/')  # each banner has titel, info, background_image, type
    banners_select = [b for b in banners if b['banner_type'] == banner_type]

    for b in banners_select:
        if b['banner_type'] == 'nieuws':
            b['items'] = get_api_data('agenda/posts/?ordering=updated_at')[:6]
        elif b['banner_type'] == 'events':
            b['items'] = get_api_data('agenda/events/?ordering=datum')[:6]
        elif b['banner_type'] == 'sponsor':
            b['items'] = get_api_data('stichting/sponsors/')
            print(b['items'])
        elif b['banner_type'] == 'projecten':
            cursussen = get_api_data('activiteiten/cursussen/')
            workshops = get_api_data('activiteiten/workshops/')
            projecten = get_api_data('activiteiten/projecten/')
            groepen = get_api_data('activiteiten/cursussen/')
            for c in cursussen:
                c['type'] = 'cursus'
            for w in workshops:
                w['type'] = 'workshop'
            for p in projecten:
                p['type'] = 'project'
            for g in groepen:
                g['type'] = 'groep'
            b['items'] = (cursussen + workshops + projecten + groepen)[:6]

    return banners_select

def home(request):
    news = get_banners('nieuws')
    events = get_banners('events')
    projects = get_banners('projecten')
    sponsors = get_banners('sponsor')
    sorted_banners = news + events + projects + sponsors
    context = {
        'headers': get_api_data('muziekschool/headers/'),
        'banners': sorted_banners,
    }
    return render(request, 'main/home.html', context)

def contact(request):
    if request.method == 'POST':
        data = {
            'naam': request.POST.get('naam'),
            'email': request.POST.get('email'),
            'bericht': request.POST.get('bericht'),
        }
        response = post_api_data('inbox/berichten/', data)
        if response and response.status_code == 201:
            messages.success(request, 'Uw bericht is succesvol verzonden!')
        else:
            messages.error(request, 'Er is een fout opgetreden. Probeer het opnieuw.')
    
    context = {}
    return render(request, 'main/contact.html', context)

