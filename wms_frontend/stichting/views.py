# stichting/views.py
from django.shortcuts import render
from api_client.views import get_api_data
from main.views import get_banners

def over_ons(request):
    context = {
        'over_info': get_api_data('muziekschool/over/'),
    }
    return render(request, 'stichting/over_ons.html', context)

def sponsors(request):
    sponsors = get_banners('sponsor')
    context = {
        'banners': sponsors,
    }
    return render(request, 'stichting/partners.html', context)

def stichting(request):
    anbi = get_api_data('stichting/anbi')
    context = {
        'anbis': anbi,
    }
    return render(request, 'stichting/stichting.html', context)