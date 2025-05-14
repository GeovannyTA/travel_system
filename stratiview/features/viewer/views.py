from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stratiview.models import UserArea, UserRol, PanoramaMetadata, Route, UserRoute
import math
from django.shortcuts import render
from django.urls import reverse
from stratiview.features.utils.utils import soft_redirect
from django.db.models.functions import Lower
from django.http import JsonResponse
from itertools import combinations
from stratiview.features.utils_amazon import generate_url_presigned
from django.contrib import messages


@login_required
def viewer(request, route_id):
    # Verificar si el usuario tiene acceso a la ruta
    user_areas = set(
        UserArea.objects.filter(user=request.user)
        .annotate(lower_area=Lower("area__name"))
        .values_list("lower_area", flat=True)
    )
    user_roles = set(
        UserRol.objects.filter(user=request.user)
        .annotate(lower_rol=Lower("rol__name"))
        .values_list("lower_rol", flat=True)
    )

    is_admin = "administrador" in user_roles or "administracion" in user_areas

    if is_admin:
        # Admin puede ver cualquier ruta
        route = Route.objects.filter(id=route_id).first()
    else:
        # Usuarios normales: solo rutas asociadas
        route = Route.objects.filter(
            id__in= UserRoute.objects.filter(user=request.user).values_list("route_id", flat=True),
        ).first()

    if not route:
        if is_admin:
            messages.warning(request, "No se ha encontrado el recorrido solicitado")
            return soft_redirect(reverse("routes"))
        else:
            messages.warning(request, "No tienes acceso a este recorrido o no existe")
            return soft_redirect(reverse("routes"))

    return render(request, 'viewer/viewer.html', {"route": route})


# @login_required
def get_nodes(request, route_id):
    # Obtener el ID de la ruta
    if request.method == "GET":
        # Precargar las relaciones necesarias para evitar consultas extra
        panoramas = PanoramaMetadata.objects.filter(route_id=route_id, is_deleted=False)

        # Preparar nodos
        for node in panoramas:
            node.url = generate_url_presigned(node.name)
        
        user_areas = set(
            UserArea.objects.filter(user=request.user)
            .annotate(lower_area=Lower("area__name"))
            .values_list("lower_area", flat=True)
        )
        user_roles = set(
            UserRol.objects.filter(user=request.user)
            .annotate(lower_rol=Lower("rol__name"))
            .values_list("lower_rol", flat=True)
        )

        is_admin = "administrador" in user_roles or "administracion" in user_areas
        if is_admin:
            nodes = [
                {
                    "id": node.id,
                    "panorama": generate_url_presigned(node.name),
                    "gps": [node.gps_lng, node.gps_lat],
                    "caption": node.name,
                    "title": node.name,
                    "altitude": node.gps_alt,
                    "direction": node.gps_direction,
                    "route": node.route.name,
                    "sphereCorrection": {"pan": f"{node.gps_direction}deg" if node.gps_direction is not None else "0deg"},
                    "links": []
                }
                for node in panoramas
            ]
        else:
            nodes = [
                {
                    "id": node.id,
                    "panorama": generate_url_presigned(node.name),
                    "gps": [node.gps_lng, node.gps_lat],
                    "altitude": node.gps_alt,
                    "direction": node.gps_direction,
                    "route": node.route.name,
                    "sphereCorrection": {"pan": f"{node.gps_direction}deg" if node.gps_direction is not None else "0deg"},
                    "links": []
                }
                for node in panoramas
            ]

        # Calcular conexiones entre nodos (optimizando combinaciones únicas)
        for node_a, node_b in combinations(nodes, 2):
            dist = distance(node_a['gps'], node_b['gps'])
            if dist <= 16:
                node_a['links'].append({"nodeId": node_b['id']})
                node_b['links'].append({"nodeId": node_a['id']})

        return JsonResponse(nodes, safe=False)
        

# Calcular distancia entre dos puntos GPS
def distance(gps1, gps2):
    R = 6371e3  # Radio de la Tierra en metros
    lat1 = math.radians(gps1[1])
    lat2 = math.radians(gps2[1])
    delta_lat = math.radians(gps2[1] - gps1[1])
    delta_lng = math.radians(gps2[0] - gps1[0])

    a = math.sin(delta_lat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c  # distancia en metros