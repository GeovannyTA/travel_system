from django.shortcuts import render
from app.models import panorama_metadata
from django.http import HttpResponse

def get_panoramas(request):
    # Fetch all panorama metadata from the database
    panoramas = panorama_metadata.objects.all()
    # Pass the panorama metadata to the template context
    context = {
        'panoramas': panoramas,
    }

    return render(request, 'panoramas/panoramas.html', context=context)

# Extract the metadata from the panorama image
def add_panoramas(request):
    panoramas = request.FILES.getlist('images')
    
    
    for panorama in panoramas:
        print("Panorama: ", panorama.name)
    return  HttpResponse("Panoramas added successfully!")