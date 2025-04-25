from django.shortcuts import redirect
from django.urls import reverse

EXCLUDED_PATHS = [
    '/stratiview/auth/sign_in/',
    '/stratiview/auth/sign_out/',
    '/stratiview/auth/password_change/',
]

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if (
            user.is_authenticated
            and user.must_change_password
            and request.path not in EXCLUDED_PATHS
            and not request.path.startswith('/admin/')  # por si usas el admin
        ):
            return redirect(reverse('password_change'))

        return self.get_response(request)