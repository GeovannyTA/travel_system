from django.http import JsonResponse
from stratiview.models import PanoramaPropertyMakers, PanoramaMetadata, PanoramaTourMarkers


def add_marker(request):
    node_id = request.GET.get('marker-node')
    key = request.GET.get('marker-key')
    account = request.GET.get('marker-account')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')

    if not node_id or not key or not account or not yaw or not pitch :
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)
    
    try:
        PanoramaPropertyMakers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            key=key,
            account=account,
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

    if not node_id or not yaw or not pitch or not type:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)
    
    try:
        PanoramaTourMarkers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            type=type,
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
            "route_name": panorama_obj.route.name if panorama_obj.route else None,
            "route_id": panorama_obj.route.id if panorama_obj.route else None
        }
        for marker in markers
    ]

    return JsonResponse(data, safe=False)