from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'branding': request.build_absolute_uri('branding/'),
        'agenda': request.build_absolute_uri('agenda/'),
        'inbox': request.build_absolute_uri('inbox/'),
        'knack': request.build_absolute_uri('knack/'),
        'muziekschool': request.build_absolute_uri('muziekschool/'),
        'stichting': request.build_absolute_uri('stichting/'),
    })