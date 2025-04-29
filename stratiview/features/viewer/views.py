from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stratiview.models import PanoramaMetadata, UserRoute, Route
from django.http import JsonResponse
import math
from django.shortcuts import render
from django.urls import reverse
from stratiview.features.utils.utils import soft_redirect


@login_required
def viewer(request):
    return render(request, 'viewer/viewer.html')


@login_required
def get_nodes(request):
    if request.method == "GET":
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return soft_redirect(reverse("viewer"))
        
        # Obtener las rutas o ruta del usuario
        routes = Route.objects.filter(
            id__in = UserRoute.objects.filter(user=request.user).values_list('route', flat=True)
        )
        
        nodes = []
        for node in PanoramaMetadata.objects.filter(route__in=routes):
            nodes.append({
                        "id": node.id,
                        "panorama": node.url,
                        "name": f"Imagen {node.id}",
                        "caption": f"Imagen {node.id}",
                        "gps": [node.gps_lng, node.gps_lat],
                        "altitude": node.gps_alt,
                        "direction": node.gps_direction,
                        "sphereCorrection": {
                            "pan": f"{node.gps_direction}deg"
                        },
                        "links": [] 
                    })
        
        # Calcular los links entre los nodos basado en la distancia GPS
        # Si la distancia entre dos nodos es menor a 10.7 metros, se crea un link entre ellos
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    continue

                dist = distance(nodes[i]['gps'], nodes[j]['gps'])

                if dist <= 10.7:
                    nodes[i]['links'].append({"nodeId": nodes[j]['id']})

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