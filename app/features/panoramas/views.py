from django.shortcuts import render
from app.models import panorama_metadata
from django.http import HttpResponse, JsonResponse
from PIL import Image, ExifTags
from app.features.utils_amazon import upload_image_to_s3
from django.db import transaction
from app.features.panoramas.utils import extract_metadata

def get_panoramas(request):
    # Fetch all panorama metadata from the database
    panoramas = panorama_metadata.objects.all()
    # Pass the panorama metadata to the template context
    context = {
        "panoramas": panoramas,
    }

    return render(request, "panoramas/panoramas.html", context=context)


# Extract the metadata from the panorama image
def add_panoramas(request):
    panoramas = request.FILES.getlist("images")
    response_data = []

    for panorama_file in panoramas:
        try:
            metadata = extract_metadata(panorama_file)
            if not metadata:
                return HttpResponse("Metadatos inválidos o incompletos.")

            # Subir imagen (rebobinar antes por si fue leída)
            panorama_file.seek(0)
            url = upload_image_to_s3(panorama_file)

            try:
                with transaction.atomic():
                    panorama_metadata.objects.create(
                        url=url,
                        gps_lat=metadata["lat"],
                        gps_lng=metadata["lon"],
                        gps_alt=metadata["alt"],
                        gps_direction=metadata["direccion"],
                        orientation=metadata["orientacion"],
                        camera_make=metadata["marca"],
                        camera_model=metadata["model"],
                        software=metadata["software"],
                        date_taken=metadata["fecha"],
                    )
            except Exception as e:
                print(f"Error al guardar los metadatos: {e}")

        except Exception as e:
            print(f"Error al procesar la imagen: {e}")

    return JsonResponse(response_data, safe=False)