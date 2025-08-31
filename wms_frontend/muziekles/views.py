# muziekles/views.py
from django.shortcuts import render
from django.contrib import messages
from api_client.views import get_api_data, post_api_data

def proefles(request):
    if request.method == 'POST':
        data = {
            'naam': request.POST.get('naam'),
            'instrument': request.POST.get('instrument'),
            'telefoon': request.POST.get('telefoon'),
            'email': request.POST.get('email'),
        }
        response = post_api_data('inbox/proeflessen/', data)
        if response and response.status_code == 201:
            messages.success(request, 'Uw proefles aanvraag is succesvol verzonden!')
        else:
            messages.error(request, 'Er is een fout opgetreden. Probeer het opnieuw.')
    
    context = {
        'instrumenten': get_api_data('knack/instrumenten/'),
    }
    return render(request, 'muziekles/proefles.html', context)

def inschrijven(request):
    voorwaarden = get_api_data('muziekschool/voorwaarden')
    inschrijven_modal = [v for v in voorwaarden if v['titel'] == 'Inschrijving']
    if inschrijven_modal:
        inschrijven_modal = inschrijven_modal[0]
    if request.method == 'POST':
        betalingsplichtige_data = {
            'initialen': request.POST.get('initialen'),
            'achternaam': request.POST.get('b_achternaam'),
            'adres': request.POST.get('adres'),
            'postcode': request.POST.get('postcode'),
            'iban': request.POST.get('iban'),
            'plaats': request.POST.get('plaats'),
            'haarlempas': request.POST.get('haarlempas') == 'on',
            'akkoord': request.POST.get('akkoord') == 'on',
        }
        betalingsplichtige_response = post_api_data('inbox/betalingsplichtigen/', betalingsplichtige_data)
        if betalingsplichtige_response and betalingsplichtige_response.status_code == 201:
            betalingsplichtige_id = betalingsplichtige_response.json()['id']
            inschrijving_data = {
                'voornaam': request.POST.get('voornaam'),
                'achternaam': request.POST.get('achternaam'),
                'instrument': request.POST.get('instrument'),
                'lestype': request.POST.get('lestype'),
                'email': request.POST.get('email'),
                'telefoon': request.POST.get('telefoon'),
                'geboortedatum': request.POST.get('geboortedatum'),
                'huren': request.POST.get('huren') == 'on',
                'betalingsplichtige': betalingsplichtige_id,
            }
            inschrijving_response = post_api_data('inbox/inschrijvingen/', inschrijving_data)
            if inschrijving_response and inschrijving_response.status_code == 201:
                messages.success(request, 'Uw inschrijving is succesvol verzonden!')
            else:
                messages.error(request, 'Er is een fout opgetreden bij de inschrijving.')
        else:
            messages.error(request, 'Er is een fout opgetreden. Probeer het opnieuw.')
    
    context = {
        'instrumenten': get_api_data('knack/instrumenten/'),
        'lestypes': get_api_data('knack/lestypes/'),
        'inschrijven_modal': inschrijven_modal,
    }
    return render(request, 'muziekles/inschrijven.html', context)


def instrumenten(request):
    context = {
        'instrumenten': get_api_data('knack/instrumenten/'),
    }
    return render(request, 'muziekles/instrumenten.html', context)

def tarieven(request):
    lestypes = get_api_data('knack/lestypes/')
    lestarieven = get_api_data('knack/lestarieven/')
    voorwaarden = get_api_data('muziekschool/voorwaarden')
    tarieven_modal = [v for v in voorwaarden if v['titel'] == 'Tarieven']
    tarieven_modal = tarieven_modal[0] if tarieven_modal else tarieven_modal
    betaling_modal = [v for v in voorwaarden if v['titel'] == 'Betaling']
    betaling_modal = betaling_modal[0] if betaling_modal else betaling_modal
    unique_soorten = []
    unique_aantallen = []
    soort_labels = {
        'IND': 'Individueel',
        'DUO': 'Duo', 
        'TRIO': 'Trio',
        'GROEP': 'Groep',
        'BAND': 'Band'
    }
    if lestypes:
        unique_soorten = list(set([lestype['soort'] for lestype in lestypes]))
        unique_soorten.sort()
        unique_aantallen = list(set([lestype['aantal'] for lestype in lestypes]))
        unique_aantallen.sort()

    filter_options = [
        {'value': soort, 'label': soort_labels.get(soort, soort)} 
        for soort in unique_soorten
    ]
    context = {
        'lestypes': lestypes,
        'lestarieven': lestarieven,
        'filter_options': filter_options,
        'unique_aantallen': unique_aantallen,
        'soort_labels': soort_labels,
        'tarieven_modal': tarieven_modal,
        'betaling_modal': betaling_modal,
    }
    return render(request, 'muziekles/tarieven.html', context)

def locaties(request):
    locaties = get_api_data('knack/locaties')
    context = {
        'locaties': locaties,
    }
    return render(request, 'muziekles/locaties.html', context)

def vacatures(request):
    context = {
        'vacatures': get_api_data('muziekschool/vacatures/'),
    }
    return render(request, 'muziekles/vacatures.html', context)