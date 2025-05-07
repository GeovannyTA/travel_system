from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from stratiview.models import User, PanoramaMetadata, UserRol, UserArea, Route, UserRoute
from stratiview.features.utils_amazon import upload_image_to_s3
from django.db import transaction
from stratiview.features.panoramas.utils import extract_metadata, calculate_distance_meters, send_upload_and_not_upload_panoramas
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix
from django.db.models.functions import Lower
from stratiview.features.utils.utils import soft_redirect
from stratiview.features.utils_amazon import generate_url_presigned
from django.core.paginator import Paginator

@login_required
@area_matrix(rules=[
    {"areas": ["administracion", "sistemas"], "methods": ["GET"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["GET"]},
])
def get_panoramas(request):
    user_areas = set(
        UserArea.objects.filter(user=request.user)
        .annotate(lower_area=Lower('area__name'))
        .values_list('lower_area', flat=True)
    )

    user_roles = set(
        UserRol.objects.filter(user=request.user)
        .annotate(lower_rol=Lower('rol__name'))
        .values_list('lower_rol', flat=True)
    )

    if any(area in ["administracion"] for area in user_areas) or any(role in ["administrador"] for role in user_roles):
        routes = Route.objects.all()
        panoramas = PanoramaMetadata.objects.select_related('route', 'upload_by').order_by("-date_uploaded")
    else:
        routes = Route.objects.filter(id=UserRoute.objects.filter(id=request.user.id))
        panoramas = PanoramaMetadata.objects.select_related('route', 'upload_by').filter(
            upload_by=request.user
        ).order_by("-date_uploaded")

    # Filtros
    route_id = request.GET.get("route_id")
    upload_by_id = request.GET.get("upload_by")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")

    if route_id:
        panoramas = panoramas.filter(route_id=route_id)

    if upload_by_id:
        panoramas = panoramas.filter(upload_by_id=upload_by_id)

    if start_date:
        panoramas = panoramas.filter(date_taken__date__gte=start_date)

    if end_date:
        panoramas = panoramas.filter(date_taken__date__lte=end_date)

    if latitude:
        panoramas = panoramas.filter(gps_lat__icontains=latitude)
    
    if longitude:
        panoramas = panoramas.filter(gps_lng__icontains=longitude)

    # Obtener usuarios únicos
    users = User.objects.filter(id__in=panoramas.values_list("upload_by", flat=True).distinct())

    # Paginación
    paginator = Paginator(panoramas, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop("page", None)
    query_string = querydict.urlencode()

    # Rango de páginas para el paginador inteligente
    current = page_obj.number
    total = paginator.num_pages

    start = max(current - 2, 1)
    end = min(current + 2, total) + 1  # +1 porque range no incluye el último

    page_range = range(start, end)

    context = {
        "panoramas": page_obj,
        "routes": routes,
        "users": users,
        "paginator": paginator,
        "query_string": query_string,
        "page_range": page_range,
        "total_pages": total,
    }
    return render(request, "panoramas/panoramas.html", context)


"""
No se implementan los decoradores de permisos para la siguiente funcion ya que 
se utiliza en el frontend para obtener los metadatos de la panorama y no se 
requiere permisos especiales para acceder a ella.
"""


@login_required
def get_panorama(request, panorama_id):
    if request.method == "GET":
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return soft_redirect(reverse("panoramas"))

        panorama = (
            PanoramaMetadata.objects.select_related("route")
            .only(
                "id",
                "route",
                "name",
                "gps_lat",
                "gps_lng",
                "gps_alt",
                "gps_direction",
                "orientation",
                "is_deleted",
            )
            .filter(id=panorama_id)
            .first()
        )
        if not panorama:
            return JsonResponse({})

        return JsonResponse(
            {
                "id": panorama.id,
                "route_id": panorama.route.id,
                "route_name": panorama.route.name,
                "panorama_name": panorama.name,
                "latitude": panorama.gps_lat,
                "longitude": panorama.gps_lng,
                "altitude": panorama.gps_alt,
                "direction": panorama.gps_direction,
                "orientation": panorama.orientation,
                "url": generate_url_presigned(panorama.name),
                "is_deleted": panorama.is_deleted,
            }
        )


@login_required
@area_matrix(
    rules=[
        {"areas": ["administracion"], "methods": ["POST"]},
    ]
)
@role_matrix(
    rules=[
        {"roles": ["administrador"], "methods": ["POST"]},
    ]
)
def add_panoramas(request):
    if request.method == "POST":
        # Obtener los archivos de imagen del formulario
        panoramas = request.FILES.getlist("images")
        route_id = request.POST.get("route")

        if not route_id:
            messages.warning(request, "No se seleccionó la ruta")
            return soft_redirect(reverse("panoramas"))

        # Obtener la entidad federativa seleccionada
        route_obj = Route.objects.get(id=route_id)

        # Arreglo para las imagenes que no se subieron
        not_uploaded = []
        uploaded = []

        for panorama_file in panoramas:
            # Extraer metadatos de la imagen
            metadata = extract_metadata(panorama_file)

            # Si no se pudieron extraer los metadatos, agregar a la lista de no subidos
            if not metadata:
                not_uploaded.append(
                    {
                        "name": panorama_file.name,
                        "error": "No se pudieron extraer los metadatos de la imagen",
                    }
                )
                continue

            # Generar el nombre del panorama
            gps_lat = metadata["lat"]
            gps_lng = metadata["lon"]
            gps_alt = metadata["alt"]
            file_name = (
                f"{gps_lat}_{gps_lng}_{gps_alt}_{route_obj.name.replace(' ', '_')}"
            )

            # Obtener todos los panoramas del estado una sola vez
            existing_panoramas = list(PanoramaMetadata.objects.filter(route=route_obj))

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
                if distance < 10:
                    nearby = True
                    break

            # Si es duplicado exacto
            if duplicate:
                not_uploaded.append(
                    {
                        "name": panorama_file.name,
                        "error": "La imagen ya existe en la base de datos",
                    }
                )
                continue

            # Si está demasiado cerca de otra imagen
            if nearby:
                not_uploaded.append(
                    {
                        "name": panorama_file.name,
                        "error": "La panoramas está demasiado cerca de otra imagen",
                    }
                )
                continue

            # Almacenar la panorama y sus metadastos en la db
            try:
                # Si falla algo no almacenar la iamgen en la db
                with transaction.atomic():
                    # Almacennar en la variable uploaded para enviar el correo

                    panorama_file.seek(0)  # Ensure the file pointer is at the beginning
                    upload_image_to_s3(panorama_file, file_name)
                    PanoramaMetadata.objects.create(
                        name=file_name,
                        gps_lat=float(metadata["lat"]),
                        gps_lng=float(metadata["lon"]),
                        gps_alt=float(metadata["alt"]),
                        gps_direction=float(metadata["direction"]),
                        orientation=float(metadata["orientation"]),
                        camera_make=metadata["marca"],
                        camera_model=metadata["model"],
                        software=metadata["software"],
                        date_taken=metadata["date_taken"],
                        route=route_obj,
                        upload_by=request.user,
                        is_deleted=False,
                    )

                    uploaded.append(
                        {
                            "name": panorama_file.name,
                        }
                    )
            except PanoramaMetadata.DoesNotExist:
                messages.warning(request, "No se pudo guardar la panorama.")
                return soft_redirect(reverse("panoramas"))
            except Exception as e:
                messages.warning(request, f"Error al guardar la panorama: {e}")
                return soft_redirect(reverse("panoramas"))

        # Enviar correo con las panoramas subidas y no subidas
        if uploaded or not_uploaded:
            send_upload_and_not_upload_panoramas(
                not_upload_panoramas=not_uploaded,
                upload_panoramas=uploaded,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
            )

        # Redirigir a la página anterior o a una URL predeterminada
        return soft_redirect(reverse("panoramas"))


@login_required
@area_matrix(
    rules=[
        {"areas": ["administracion"], "methods": ["POST"]},
    ]
)
def edit_panorama(request):
    if request.method == "POST":
        panorama_id = request.POST.get("edit-panorama_id")
        panorama = PanoramaMetadata.objects.get(id=panorama_id)
        action = request.POST.get("action")

        if action == "enable":
            panorama.is_deleted = False
            panorama.save()
            messages.info(request, "Panorama habilitado correctamente")
            return soft_redirect(reverse("panoramas"))
        

        if action == "save":
            latitude = request.POST.get("edit-latitude")
            longitude = request.POST.get("edit-longitude")
            route = request.POST.get("edit-route")
            direction = request.POST.get("edit-direction")
            if latitude:
                panorama.gps_lat = latitude

            if longitude:
                panorama.gps_lng = longitude

            if route:
                route_obj = Route.objects.filter(id=route).first()
                if route_obj:
                    panorama.route = route_obj

            if direction:
                panorama.gps_direction = direction

            panorama.save()
            messages.info(request, "Panorama editado correctamente")
            return soft_redirect(reverse("panoramas"))


@login_required
@area_matrix(
    rules=[
        {"areas": ["administracion"], "methods": ["POST"]},
    ]
)
def delete_panorama(request):
    if request.method == "POST":
        panorama_id = request.POST.get("panorama_id")
        panorama = PanoramaMetadata.objects.get(id=panorama_id)

        if not panorama:
            messages.warning(request, "Panorama no encontrado.")
            return soft_redirect(reverse("panoramas"))

        panorama.is_deleted = True
        panorama.save()
        messages.info(request, "Panorama eliminado correctamente")
        return soft_redirect(reverse("panoramas"))
