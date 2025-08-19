# activiteiten/views.py
from django.shortcuts import render
from api_client.views import get_api_data, normalize_item

def cursussen(request):
    cursussen = get_api_data('activiteiten/cursussen/')
    for c in cursussen:
        c['type'] = 'cursus'
    context = {
        'cursussen': cursussen,
        'instrumenten': cursussen,
    }
    return render(request, 'activiteiten/cursussen.html', context)

def cursus_detail(request, id):
    cursus_data = get_api_data(f'activiteiten/cursussen/{id}/')
    if not cursus_data:
        return render(request, 'main/404.html', status=404)
    
    context = {'cursus': normalize_item(cursus_data)}
    return render(request, 'activiteiten/cursus_detail.html', context)

def workshops(request):
    workshops = get_api_data('activiteiten/workshops/')
    for w in workshops:
        w['type'] = 'workshop'
    context = {
        'workshops': workshops,
    }
    return render(request, 'activiteiten/workshops.html', context)

def workshop_detail(request, id):
    workshop_data = get_api_data(f'activiteiten/workshops/{id}/')
    if not workshop_data:
        return render(request, 'main/404.html', status=404)
    
    context = {
        'workshop': normalize_item(workshop_data),
    }
    return render(request, 'activiteiten/workshop_detail.html', context)

def projecten(request):
    projects = get_api_data('activiteiten/projecten/')
    for p in projects:
        p['type'] = 'project'
    context = {
        'projecten': projects,
    }
    return render(request, 'activiteiten/projecten.html', context)

def project_detail(request, id):
    project_data = get_api_data(f'activiteiten/projecten/{id}/')
    if not project_data:
        return render(request, 'main/404.html', status=404)
    
    context = {
        'project': normalize_item(project_data),
    }
    return render(request, 'activiteiten/project_detail.html', context)

def groepen(request):
    groepen = get_api_data('activiteiten/groepen/')
    for g in groepen:
        g['type'] = 'groep'
    context = {
        'groepen': groepen,
    }
    return render(request, 'activiteiten/groepen.html', context)

def groep_detail(request, id):
    groep_data = get_api_data(f'activiteiten/groepen/{id}/')
    if not groep_data:
        return render(request, 'main/404.html', status=404)
    
    context = {'groep': normalize_item(groep_data)}
    return render(request, 'activiteiten/groep_detail.html', context)

