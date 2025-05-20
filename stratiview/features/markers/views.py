from django.http import JsonResponse
from stratiview.models import PanoramaPropertyMakers, PanoramaMetadata, PanoramaTourMarkers, Route, PanoramaObjectMarkers


def add_marker(request):
    node_id = request.GET.get('marker-node')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')
    updated_use = request.GET.get('marker-type-current_use')  # corresponde a updated_use
    property_type = request.GET.get('marker-type')  # tipo de predio
    size = request.GET.get('marker-size')
    business_name = request.GET.get('marker-name')
    land_position = request.GET.get('marker-position')
    observation = request.GET.get('marker-observation')

    if not all([node_id, yaw, pitch, updated_use, property_type]):
        return JsonResponse({'error': 'Faltan parámetros obligatorios'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()
    if not panorama_obj:
        return JsonResponse({'error': 'Panorama no encontrado'}, status=404)

    try:
        PanoramaPropertyMakers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            updated_use=updated_use,  # debe estar en minúsculas por las CHOICES
            property_type=property_type,
            size=size if size else None,
            business_name=business_name,
            land_position=land_position if land_position else None,
            observation=observation
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'success': True})


def get_markers(request):
    node_id = request.GET.get('marker-node')
    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)

    markers = PanoramaPropertyMakers.objects.filter(panorama=panorama_obj).values()
    return JsonResponse(list(markers), safe=False)


def add_route_marker(request):
    node_id = request.GET.get('marker-node')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')
    type = request.GET.get('marker-type')
    route_id = request.GET.get('marker-route')

    if not node_id or not yaw or not pitch or not type or not route_id:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()
    route_obj = Route.objects.filter(id=route_id).first()

    if not panorama_obj or not route_obj:
        return JsonResponse({'error': 'Panorama or Route not found'}, status=404)
    
    try:
        PanoramaTourMarkers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            type=type,
            route=route_obj,
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'success': True})


def get_route_markers(request):
    node_id = request.GET.get('marker-node')
    panorama_obj = PanoramaMetadata.objects.select_related('route').filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)

    markers = PanoramaTourMarkers.objects.filter(panorama=panorama_obj)

    # Construye la respuesta incluyendo el nombre de la ruta
    data = [
        {
            "id": marker.id,
            "yaw": marker.yaw,
            "pitch": marker.pitch,
            "type": marker.type,
            "panorama_id": marker.panorama.id,
            "route_name": marker.route.name if marker.route else None,
            "route_id": marker.route.id if marker.route else None
        }
        for marker in markers
    ]

    return JsonResponse(data, safe=False)


def add_object_marker(request):
    node_id = request.GET.get('marker-node')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')
    name = request.GET.get('marker-name')
    description = request.GET.get('marker-description')

    if not node_id or not yaw or not pitch or not name or not description:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)
    
    try:
        PanoramaObjectMarkers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            name=name,
            description=description
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'success': True})


def get_object_markers(request):
    node_id = request.GET.get('marker-node')
    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)

    markers = PanoramaObjectMarkers.objects.filter(panorama=panorama_obj).values()
    return JsonResponse(list(markers), safe=False)