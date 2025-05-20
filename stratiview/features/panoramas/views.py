from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from stratiview.models import User, PanoramaMetadata, UserRol, UserArea, Route, UserRoute
from stratiview.features.utils_amazon import upload_image_to_s3
from django.db import transaction
from stratiview.features.panoramas.utils import extract_metadata, calculate_distance_meters, send_upload_and_not_upload_panoramas, calculate_decimal_range
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix
from django.db.models.functions import Lower
from stratiview.features.utils.utils import soft_redirect
from stratiview.features.utils_amazon import generate_url_presigned
from django.core.paginator import Paginator
from pathlib import Path

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
        try:
            lat = float(latitude)
            lat_range = calculate_decimal_range(latitude)
            panoramas = panoramas.filter(gps_lat__gte=lat - lat_range, gps_lat__lte=lat + lat_range)
        except ValueError:
            pass

    if longitude:
        try:
            lng = float(longitude)
            lng_range = calculate_decimal_range(longitude)
            panoramas = panoramas.filter(gps_lng__gte=lng - lng_range, gps_lng__lte=lng + lng_range)
        except ValueError:
            pass

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
                "is_default",
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
                "is_default": panorama.is_default,
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
        panoramas = request.FILES.getlist("images")
        route_id = request.POST.get("route")
        force_upload = bool(request.POST.get("force_upload", False))

        if not route_id:
            messages.warning(request, "No se seleccionó la ruta")
            return soft_redirect(reverse("panoramas"))

        route_obj = Route.objects.get(id=route_id)
        not_uploaded = []
        uploaded = []

        # Coordenadas y nombres existentes (una sola consulta)
        existing_data = list(
            PanoramaMetadata.objects.filter(route=route_obj)
            .values_list("name", "gps_lat", "gps_lng", "gps_alt")
        )
        existing_coords = [(lat, lon, alt) for _, lat, lon, alt in existing_data]
        existing_names = {name for name, _, _, _ in existing_data}

        new_metadata_objects = []

        for panorama_file in panoramas:
            metadata = extract_metadata(panorama_file)

            if not metadata:
                not_uploaded.append({
                    "name": panorama_file.name,
                    "error": "No se pudieron extraer los metadatos de la imagen",
                })
                continue

            gps_lat = float(metadata["lat"])
            gps_lng = float(metadata["lon"])
            gps_alt = float(metadata["alt"])
            file_name = f"{Path(panorama_file.name).stem}-{route_obj.name.replace(' ', '_')}"

            # Verificar duplicado exacto
            if (
                file_name in existing_names or
                (gps_lat, gps_lng, gps_alt) in existing_coords
            ):
                not_uploaded.append({
                    "name": file_name,
                    "error": "La imagen ya existe en la base de datos",
                })
                continue
            
            if force_upload == False:
                # Verificar si está demasiado cerca de alguna ya registrada
                is_near = any(
                    calculate_distance_meters(gps_lat, gps_lng, gps_alt, lat2, lon2, alt2) < 10
                    for lat2, lon2, alt2 in existing_coords
                )
                if is_near:
                    not_uploaded.append({
                        "name": file_name,
                        "error": "La panorama está demasiado cerca de otra imagen",
                    })
                    continue

            try:
                panorama_file.seek(0)
                upload_image_to_s3(panorama_file, file_name)

                new_metadata_objects.append(
                    PanoramaMetadata(
                        name=file_name,
                        gps_lat=gps_lat,
                        gps_lng=gps_lng,
                        gps_alt=gps_alt,
                        gps_direction=float(metadata["direction"]),
                        orientation=float(metadata["orientation"]),
                        camera_make=metadata["marca"],
                        camera_model=metadata["model"],
                        software=metadata["software"],
                        date_taken=metadata["date_taken"],
                        route=route_obj,
                        upload_by=request.user,
                        is_deleted=False,
                        is_default=False
                    )
                )

                uploaded.append({ "name": panorama_file.name })
                # Agregar a sets/listas locales para próximas verificaciones
                existing_coords.append((gps_lat, gps_lng, gps_alt))
                existing_names.add(file_name)

            except Exception as e:
                not_uploaded.append({
                    "name": panorama_file.name,
                    "error": f"Error al guardar la panorama: {str(e)}"
                })

        if new_metadata_objects:
            try:
                with transaction.atomic():
                    PanoramaMetadata.objects.bulk_create(new_metadata_objects)
            except Exception as e:
                messages.warning(request, f"Error al guardar panoramas: {str(e)}")

        if uploaded or not_uploaded:
            send_upload_and_not_upload_panoramas(
                not_upload_panoramas=not_uploaded,
                upload_panoramas=uploaded,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
            )

        return soft_redirect(reverse("panoramas"))


def is_nearby(gps_lat, gps_lng, gps_alt, existing_coords):
    for lat2, lon2, alt2 in existing_coords:
        distance = calculate_distance_meters(gps_lat, gps_lng, gps_alt, lat2, lon2, alt2)
        if distance < 10:  # distancia mínima en metros
            return True
    return False

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
            is_default = request.POST.get("is_default")

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

            if is_default:
                PanoramaMetadata.objects.filter(route=panorama.route).update(is_default=False)
                panorama.is_default = True

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
