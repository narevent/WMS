from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

@csrf_exempt
@login_required
def tinymce_upload(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']

        filename = default_storage.save(
            f'tinymce/{uploaded_file.name}', 
            uploaded_file
        )
        
        return JsonResponse({
            'location': f'/media/api/{filename}'
        })
    
    return JsonResponse({'error': 'No file uploaded'}, status=400)