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



def get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1]
    seconds = dms[2][0] / dms[2][1]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in [b'S', b'W']:
        decimal = -decimal
        
    return decimal