# Forzar redireccion a la pagina de home si el usuario ya esta autenticado
from django.shortcuts import redirect
from django.urls import reverse

class ForceRedirectHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/auth/sign_in/':
            return redirect(reverse('home'))
        
        return self.get_response(request)