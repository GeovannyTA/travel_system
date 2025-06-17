from django.shortcuts import render
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
from django.db.models.expressions import RawSQL
from django.contrib.auth.decorators import login_required

@login_required
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
            id__in=UserRoute.objects.filter(user=request.user).values_list(
                "route_id", flat=True
            ),
        ).first()

    if not route:
        if is_admin:
            messages.warning(request, "No se ha encontrado el recorrido solicitado")
            return soft_redirect(reverse("routes"))
        else:
            messages.warning(request, "No tienes acceso a este recorrido o no existe")
            return soft_redirect(reverse("routes"))

    return render(
        request,
        "viewer/viewer.html",
        {"route": route, "is_admin": True if is_admin else False, "node": 0},
    )


# Visor publico
def viewer_public(request, route_id):
    # Verificar si el usuario tiene acceso a la ruta
    route = Route.objects.filter(id=route_id).first()

    if not route:
        messages.warning(request, "No se ha encontrado el recorrido solicitado")
        return soft_redirect(reverse("routes"))

    return render(request, "viewer/viewer.html", {"route": route, "is_admin": False, "node": 0 })


def viewer_coordenates(request, gps_lat, gps_lng):
    gps_lat = float(gps_lat)
    gps_lng = float(gps_lng)

    # Fórmula Haversine adaptada para SQL Server con protección de rango en acos()
    haversine_sql = """
        6371 * acos(
            CASE 
                WHEN (
                    cos(radians(%s)) * cos(radians(gps_lat)) *
                    cos(radians(gps_lng) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(gps_lat))
                ) > 1 THEN 1
                WHEN (
                    cos(radians(%s)) * cos(radians(gps_lat)) *
                    cos(radians(gps_lng) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(gps_lat))
                ) < -1 THEN -1
                ELSE (
                    cos(radians(%s)) * cos(radians(gps_lat)) *
                    cos(radians(gps_lng) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(gps_lat))
                )
            END
        )
    """

    params = (
        gps_lat,
        gps_lng,
        gps_lat,  # Primer bloque
        gps_lat,
        gps_lng,
        gps_lat,  # Segundo bloque
        gps_lat,
        gps_lng,
        gps_lat,  # Else
    )

    nearby_node = (
        PanoramaMetadata.objects.annotate(distance=RawSQL(haversine_sql, params))
        .order_by("distance")
        .first()
    )

    if not nearby_node:
        return render(
            request,
            "viewer/viewer.html",
            {"error": "No se encontró una panorámica cercana."},
        )
    

    return render(
        request,
        "viewer/viewer.html", {"route":  nearby_node.route, "is_admin": False, "node": nearby_node.id}
    )


# @login_required
def get_nodes(request, route_id, node_id):
    # Obtener el ID de la ruta
    if request.method == "GET":
        route = Route.objects.filter(id=route_id).first()
        print("Tipo de recorrido get_nodes(): ", route.type.lower().replace(" ", "_"))

        # Precargar las relaciones necesarias para evitar consultas extra
        panoramas = list(PanoramaMetadata.objects.filter(route_id=route_id, is_deleted=False))
        
        if route.type.lower().replace(" ", "_") in ["interior"]:
            dist_1 = 2
            dist_2 = 5
        elif route.type.lower().replace(" ", "_") in ["a_pie"]:
            dist_1 = 9
            dist_2 = 14
        elif route.type.lower().replace(" ", "_") in ["aereo"]:
            dist_1 = 100
            dist_2 = 200
        else:
            dist_1 = 17
            dist_2 = 40

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
                    "sphereCorrection": {
                        "pan": (
                            f"{node.gps_direction}deg"
                            if node.gps_direction is not None
                            else "0deg"
                        )
                    },
                    "links": [],
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
                        "sphereCorrection": {
                            "pan": (
                                f"{node.gps_direction}deg"
                                if node.gps_direction is not None
                                else "0deg"
                            )
                        },
                        "links": [],
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
                        "sphereCorrection": {
                            "pan": (
                                f"{node.gps_direction}deg"
                                if node.gps_direction is not None
                                else "0deg"
                            )
                        },
                        "links": [],
                    }
                    for node in panoramas
                ]

        import math

        def bearing(from_coords, to_coords):
            lon1, lat1 = map(math.radians, from_coords)
            lon2, lat2 = map(math.radians, to_coords)
            dlon = lon2 - lon1
            x = math.sin(dlon) * math.cos(lat2)
            y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(
                lat2
            ) * math.cos(dlon)
            angle = math.degrees(math.atan2(x, y))
            return (angle + 360) % 360

        def is_direction_unique(existing_angles, new_angle, tolerance=40):
            return all(
                abs((a - new_angle + 180) % 360 - 180) > tolerance
                for a in existing_angles
            )
        
        # Inicializar lista de ángulos usados
        for node in nodes:
            node["used_angles"] = []

        # Primer pase: distancia + ángulo
        for node_a, node_b in combinations(nodes, 2):
            dist = distance(node_a["gps"], node_b["gps"])
            if dist <= dist_1:
                angle_a_to_b = bearing(node_a["gps"], node_b["gps"])
                angle_b_to_a = bearing(node_b["gps"], node_a["gps"])

                if is_direction_unique(node_a["used_angles"], angle_a_to_b) and \
                is_direction_unique(node_b["used_angles"], angle_b_to_a):

                    node_a["links"].append({"nodeId": node_b["id"]})
                    node_b["links"].append({"nodeId": node_a["id"]})

                    node_a["used_angles"].append(angle_a_to_b % 360)
                    node_b["used_angles"].append(angle_b_to_a % 360)

        # Segundo pase: nodos aislados
        for node_a in nodes:
            if len(node_a["links"]) <= 1:
                for node_b in nodes:
                    if node_a["id"] == node_b["id"]:
                        continue
                    dist = distance(node_a["gps"], node_b["gps"])
                    if dist <= dist_2:
                        angle_a_to_b = bearing(node_a["gps"], node_b["gps"])
                        angle_b_to_a = bearing(node_b["gps"], node_a["gps"])

                        if is_direction_unique(node_a["used_angles"], angle_a_to_b) and \
                        is_direction_unique(node_b["used_angles"], angle_b_to_a):

                            if not any(link["nodeId"] == node_b["id"] for link in node_a["links"]):
                                node_a["links"].append({"nodeId": node_b["id"]})
                            if not any(link["nodeId"] == node_a["id"] for link in node_b["links"]):
                                node_b["links"].append({"nodeId": node_a["id"]})

                            node_a["used_angles"].append(angle_a_to_b % 360)
                            node_b["used_angles"].append(angle_b_to_a % 360)

        return JsonResponse(
            {"default_node_id": default_node_id, "nodes": nodes}, safe=False
        )


# Calcular distancia entre dos puntos GPS
def distance(gps1, gps2):
    R = 6371e3  # Radio de la Tierra en metros
    lat1 = math.radians(gps1[1])
    lat2 = math.radians(gps2[1])
    delta_lat = math.radians(gps2[1] - gps1[1])
    delta_lng = math.radians(gps2[0] - gps1[0])

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distancia en metros


def get_routes(request):
    # Obtener todas las rutas
    routes = Route.objects.all()
    route_list = [{"id": route.id, "name": route.name} for route in routes]
    return JsonResponse(route_list, safe=False)


def vr_viewer(request, panorama_id):
    panorama = PanoramaMetadata.objects.get(id=panorama_id)
    panorama_url = generate_url_presigned(panorama.name)

    return render(request, "viewer/vr_viewer.html", {"panorama_url": panorama_url})