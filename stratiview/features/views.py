from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden

@login_required
def home(request):
    return render(request, 'home/home.html')


def check_sesion(request):
    if not request.user.is_authenticated:
        # Si ya no está autenticado, devolver 403 Forbidden
        return HttpResponseForbidden('Session expired')

    # Si sigue autenticado, responder OK
    return JsonResponse({'status': 'alive'})