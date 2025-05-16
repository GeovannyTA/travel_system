from django.http import JsonResponse
from stratiview.models import PanoramaMakers, PanoramaMetadata


def add_marker(request):
    node_id = request.GET.get('marker-node')
    key = request.GET.get('marker-key')
    account = request.GET.get('marker-account')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')
    type = request.GET.get('marker-type')

    if not node_id or not key or not account or not yaw or not pitch or not type:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)
    
    try:
        PanoramaMakers.objects.create(
            yaw=yaw,
            pitch=pitch,
            panorama=panorama_obj,
            key=key,
            account=account,
            type=type
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'success': True})


def get_markers(request):
    node_id = request.GET.get('marker-node')
    panorama_obj = PanoramaMetadata.objects.filter(id=node_id).first()

    if not panorama_obj:
        return JsonResponse({'error': 'Panorama not found'}, status=404)

    markers = PanoramaMakers.objects.filter(panorama=panorama_obj).values()
    return JsonResponse(list(markers), safe=False)