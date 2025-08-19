# agenda/views.py
from django.shortcuts import render
from api_client.views import get_api_data
from main.views import get_banners

def agenda(request):
    posts = get_banners('nieuws')
    events = get_banners('events')
    banners = posts + events
    context = {
        #'events': get_api_data('agenda/events/?ordering=datum'),
        #'posts': get_api_data('agenda/posts/'),
        'banners': banners,
        'vakanties': get_api_data('agenda/vakanties/'),
    }
    return render(request, 'agenda/agenda.html', context)

def event_detail(request, id):
    event_data = get_api_data(f'agenda/events/{id}/')
    if not event_data:
        return render(request, 'main/404.html', status=404)
    
    context = {
        'event': event_data,
    }
    return render(request, 'agenda/event_detail.html', context)

def post_detail(request, id):
    post_data = get_api_data(f'agenda/posts/{id}/')
    if not post_data:
        return render(request, 'main/404.html', status=404)
    
    context = {
        'post': post_data,
    }
    return render(request, 'agenda/post_detail.html', context)

def vakanties(request):
    vakanties = get_api_data('agenda/vakanties')
    context = {
        'vakanties': vakanties,
    }
    return render(request, 'agenda/vakanties.html', context)