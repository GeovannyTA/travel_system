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


# @login_required
# Modificar para que no sea necesario el login
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


# Visor publico
def viewer_public(request, route_id):
    # Verificar si el usuario tiene acceso a la ruta
    route = Route.objects.filter(id=route_id).first()

    if not route:
        messages.warning(request, "No se ha encontrado el recorrido solicitado")
        return soft_redirect(reverse("routes"))

    return render(request, 'viewer/viewer.html', {"route": route})


# @login_required
def get_nodes(request, route_id):
    # Obtener el ID de la ruta
    if request.method == "GET":
        # Precargar las relaciones necesarias para evitar consultas extra
        panoramas = list(PanoramaMetadata.objects.filter(route_id=route_id, is_deleted=False))


        default_panorama = next((p for p in panoramas if p.is_default), None)
        default_node_id = default_panorama.id if default_panorama else None

        # Preparar nodos
        if not request.user.is_authenticated:
            # Si el usuario no está autenticado, no se pueden obtener áreas o roles
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
        else:
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
            if dist <= 17:
                node_a['links'].append({"nodeId": node_b['id']})
                node_b['links'].append({"nodeId": node_a['id']})

        import math

        def bearing(from_coords, to_coords):
            lon1, lat1 = map(math.radians, from_coords)
            lon2, lat2 = map(math.radians, to_coords)
            dlon = lon2 - lon1
            x = math.sin(dlon) * math.cos(lat2)
            y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
            angle = math.degrees(math.atan2(x, y))
            return (angle + 360) % 360

        def is_direction_unique(existing_angles, new_angle, tolerance=30):
            return all(abs((a - new_angle + 180) % 360 - 180) > tolerance for a in existing_angles)
        
        # Segundo pase: nodos aislados, permitir enlaces en direcciones distintas (≤19m)
        for node_a in nodes:
            if len(node_a['links']) <= 1:
                used_angles = []
                for node_b in nodes:
                    if node_a['id'] == node_b['id']:
                        continue
                    dist = distance(node_a['gps'], node_b['gps'])
                    if dist <= 20:
                        angle = bearing(node_a['gps'], node_b['gps'])
                        if is_direction_unique(used_angles, angle):
                            if not any(link["nodeId"] == node_b["id"] for link in node_a["links"]):
                                node_a['links'].append({"nodeId": node_b['id']})
                            if not any(link["nodeId"] == node_a["id"] for link in node_b["links"]):
                                node_b['links'].append({"nodeId": node_a['id']})
                            used_angles.append(angle)

        return JsonResponse({
            "default_node_id": default_node_id,
            "nodes": nodes
        }, safe=False)
        

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


def get_routes(request):
    # Obtener todas las rutas
    routes = Route.objects.all()
    route_list = [{"id": route.id, "name": route.name} for route in routes]
    return JsonResponse(route_list, safe=False)