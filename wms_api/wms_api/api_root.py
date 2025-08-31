from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'muziekschool': request.build_absolute_uri('muziekschool/'),
        'agenda': request.build_absolute_uri('agenda/'),
        'activiteiten': request.build_absolute_uri('activiteiten/'),
        'inbox': request.build_absolute_uri('inbox/'),
        'knack': request.build_absolute_uri('knack/'),
        'stichting': request.build_absolute_uri('stichting/'),
        'branding': request.build_absolute_uri('branding/'),
    })