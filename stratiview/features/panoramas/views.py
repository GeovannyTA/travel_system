from time import strftime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from stratiview.models import PanoramaMetadata, State
from stratiview.features.utils_amazon import upload_image_to_s3
from django.db import transaction
from stratiview.features.panoramas.utils import extract_metadata, calculate_distance_meters

def get_panoramas(request):
    panoramas = PanoramaMetadata.objects.all()
    states = State.objects.all()

    # If there are no panoramas, return an empty list
    if not panoramas:
        return render(
            request,
            "panoramas/panoramas.html",
            context={"panoramas": [], "states": states},
        )

    context = {
        "panoramas": panoramas,
        "states": states,
    }

    return render(request, "panoramas/panoramas.html", context=context)


# Extract the metadata from the panorama image
def add_panoramas(request):
    if request.method == "GET":
        return HttpResponse("Método no permitido.")

    if request.method == "POST":
        # Obtener los archivos de imagen del formulario
        panoramas = request.FILES.getlist("images")
        state_id = request.POST.get("state")

        if not state_id:
            return HttpResponse("No se selecciono la entidad federativa.")

        # Obtener la entidad federativa seleccionada
        state_obj = State.objects.get(id=state_id)

        # Arreglo para las imagenes que no se subieron
        not_uploaded = []

        for panorama_file in panoramas:
            # Extraer metadatos de la imagen
            metadata = extract_metadata(panorama_file)

            # Si no se pudieron extraer los metadatos, agregar a la lista de no subidos
            if not metadata:
                not_uploaded.append(panorama_file.name)
                continue

            # Generar el nombre del panorama
            gps_lat = metadata["lat"]
            gps_lng = metadata["lon"]
            gps_alt = metadata["alt"]
            # file_name = f'{metadata["date_taken"].strftime("%Y%m%d_%H%M")}_{gps_lat}_{gps_lng}'
            file_name = f"{gps_lat}_{gps_lng}_{gps_alt}_{state_obj.name}"

            # Obtener todos los panoramas del estado una sola vez
            existing_panoramas = list(PanoramaMetadata.objects.filter(state=state_obj))

            # Verificar si ya existe uno con los mismos metadatos o está muy cerca
            duplicate = False
            nearby = False

            for existing in existing_panoramas:
                # Verificar si la imagen ya existe
                if (
                    existing.name == file_name
                    and existing.gps_lat == gps_lat
                    and existing.gps_lng == gps_lng
                    and existing.gps_alt == gps_alt
                ):
                    duplicate = True
                    break

                # Calcular la distancia de las panoramas
                distance = calculate_distance_meters(
                    gps_lat,
                    gps_lng,
                    gps_alt,
                    existing.gps_lat,
                    existing.gps_lng,
                    existing.gps_alt,
                )

                # Verificar si una panorama se encuentra muy cerca de otra
                if distance < 5:
                    nearby = True
                    break

            # Si es duplicado exacto
            if duplicate:
                print("El panorama ya existe")
                not_uploaded.append(f"{panorama_file.name}")
                continue

            # Si está demasiado cerca de otra imagen
            if nearby:
                print("El panorama se encuentra muy cerca de otro")
                not_uploaded.append(f"{panorama_file.name}")
                continue

            # Almacenar la panorama y sus metadastos en la db
            try:
                # Si falla algo no almacenar la iamgen en la db
                with transaction.atomic():
                    panorama_file.seek(0)
                    url = upload_image_to_s3(panorama_file, file_name)
                    PanoramaMetadata.objects.create(
                        url=url,
                        name=file_name,
                        gps_lat=metadata["lat"],
                        gps_lng=metadata["lon"],
                        gps_alt=metadata["alt"],
                        gps_direction=metadata["direction"],
                        orientation=metadata["orientation"],
                        camera_make=metadata["marca"],
                        camera_model=metadata["model"],
                        software=metadata["software"],
                        date_taken=metadata["date_taken"],
                        state=state_obj,
                    )
            except Exception as e:
                return HttpResponse(f"Error al guardar los metadatos.{e}")

        # Redirigir a la página anterior o a una URL predeterminada
        return redirect(request.META.get("HTTP_REFERER", "/"))
