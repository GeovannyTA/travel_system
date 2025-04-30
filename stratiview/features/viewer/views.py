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


@login_required
def viewer(request):
    return render(request, 'viewer/viewer.html')


@login_required
def get_nodes(request):
    if request.method == "GET":
        # if request.headers.get("x-requested-with") != "XMLHttpRequest":
        #     return soft_redirect(reverse("viewer"))
        
        user = request.user

        # Obtener las áreas y roles del usuario en minúscula
        user_areas = set(
            UserArea.objects.filter(user=user)
            .annotate(lower_area=Lower('area__name'))
            .values_list('lower_area', flat=True)
        )
        user_roles = set(
            UserRol.objects.filter(user=user)
            .annotate(lower_rol=Lower('rol__name'))
            .values_list('lower_rol', flat=True)
        )

        # Determinar si es administrador o no
        is_admin = "administracion" in user_areas or "administrador" in user_roles

        # Obtener las rutas correspondientes
        if is_admin:
            routes_ids = Route.objects.values_list('id', flat=True)
        else:
            routes_ids = UserRoute.objects.filter(user=user).values_list('route_id', flat=True)

        # Precargar las relaciones necesarias para evitar consultas extra
        panoramas = PanoramaMetadata.objects.select_related('route__state').filter(route_id__in=routes_ids)

        # Preparar nodos
        for node in panoramas:
            node.url = generate_url_presigned(node.name)
            
        nodes = [
            {
                "id": node.id,
                "panorama": generate_url_presigned(node.name),
                "gps": [node.gps_lng, node.gps_lat],
                "altitude": node.gps_alt,
                "direction": node.gps_direction,
                "state": node.route.state.name,
                "route": node.route.name,
                "sphereCorrection": {"pan": f"{node.gps_direction}deg" if node.gps_direction is not None else "0deg"},
                "links": []
            }
            for node in panoramas
        ]

        # Calcular conexiones entre nodos (optimizando combinaciones únicas)
        for node_a, node_b in combinations(nodes, 2):
            dist = distance(node_a['gps'], node_b['gps'])
            if dist <= 15:
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