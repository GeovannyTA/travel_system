from django.http import JsonResponse

def add_marker(request):
    key = request.GET.get('marker-key')
    account = request.GET.get('marker-account')
    yaw = request.GET.get('marker-yaw')
    pitch = request.GET.get('marker-pitch')

    print(f"Key: {key}")
    print(f"Account: {account}")
    print(f"Yaw: {yaw}")
    print(f"Pitch: {pitch}")
 
    return JsonResponse({'success': True})