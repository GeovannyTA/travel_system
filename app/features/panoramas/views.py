from time import strftime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import panorama_metadata
from app.features.utils_amazon import upload_image_to_s3
from django.db import transaction
from app.features.panoramas.utils import extract_metadata

def get_panoramas(request):
    # Fetch all panorama metadata from the database
    panoramas = panorama_metadata.objects.all()

    states = [
            { "id": "AGS", "name": "Aguascalientes" },
            { "id": "BC", "name": "Baja California" },
            { "id": "BCS", "name": "Baja California Sur" },
            { "id": "CAMP", "name": "Campeche" },
            { "id": "CHIS", "name": "Chiapas" },
            { "id": "CHIH", "name": "Chihuahua" },
            { "id": "COAH", "name": "Coahuila de Zaragoza" },
            { "id": "COL", "name": "Colima" },
            { "id": "CDMX", "name": "Ciudad de México" },
            { "id": "DGO", "name": "Durango" },
            { "id": "MEX", "name": "Estado de México" },
            { "id": "GTO", "name": "Guanajuato" },
            { "id": "GRO", "name": "Guerrero" },
            { "id": "HGO", "name": "Hidalgo" },
            { "id": "JAL", "name": "Jalisco" },
            { "id": "MIC", "name": "Michoacán de Ocampo" },
            { "id": "MOR", "name": "Morelos" },
            { "id": "NAY", "name": "Nayarit" },
            { "id": "NL", "name": "Nuevo León" },
            { "id": "OAX", "name": "Oaxaca" },
            { "id": "PUE", "name": "Puebla" },
            { "id": "QRO", "name": "Querétaro" },
            { "id": "QR", "name": "Quintana Roo" },
            { "id": "SLP", "name": "San Luis Potosí" },
            { "id": "SIN", "name": "Sinaloa" },
            { "id": "SON", "name": "Sonora" },
            { "id": "TAB", "name": "Tabasco" },
            { "id": "TAMPS", "name": "Tamaulipas" },
            { "id": "TLAX", "name": "Tlaxcala" },
            { "id": "VER", "name": "Veracruz de Ignacio de la Llave" },
            { "id": "YUC", "name": "Yucatán" },
            { "id": "ZAC", "name": "Zacatecas" }
        ]
    
    context = {
        "panoramas": panoramas,
        "states": states,
    }

    return render(request, "panoramas/panoramas.html", context=context)


# Extract the metadata from the panorama image
def add_panoramas(request):
    if request.method != "POST":
        return HttpResponse("Método no permitido.")
    
    # Obtener los archivos de imagen del formulario
    panoramas = request.FILES.getlist("images")

    for panorama_file in panoramas:
        metadata = extract_metadata(panorama_file)
        if not metadata:
            # return HttpResponse("Metadatos inválidos o incompletos.")
            continue   

        # Subir imagen (rebobinar antes por si fue leída)
        file_name = f'{metadata["date_taken"].strftime("%Y%m%d_%H%M")}_{metadata["lat"]}_{metadata["lon"]}'
        gps_lat = metadata["lat"]
        gps_lng = metadata["lon"]
        gps_alt = metadata["alt"]

        # Verificar si ya existe un panorama con los mismos metadatos
        if panorama_metadata.objects.filter(
            name=file_name,
            gps_lat=gps_lat,
            gps_lng=gps_lng,
            gps_alt=gps_alt
        ).exists():
            print(f"El panorama {file_name} ya existe en la base de datos.")
            continue

        panorama_file.seek(0)
        url = upload_image_to_s3(panorama_file, file_name)

        try:
            with transaction.atomic():
                panorama_metadata.objects.create(
                    url = url,
                    name  = file_name,
                    gps_lat = metadata["lat"],
                    gps_lng = metadata["lon"],
                    gps_alt = metadata["alt"],
                    gps_direction = metadata["direction"],
                    orientation = metadata["orientation"],
                    camera_make = metadata["marca"],
                    camera_model = metadata["model"],
                    software = metadata["software"],
                    date_taken = metadata["date_taken"],
                )
        except Exception as e:
            return HttpResponse(f"Error al guardar los metadatos.{e}")

    # Redirigir a la página anterior o a una URL predeterminada
    return redirect(request.META.get("HTTP_REFERER", "/"))