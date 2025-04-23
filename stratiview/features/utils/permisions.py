from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from stratiview.models import UserArea, UserRol
from django.contrib import messages


# Decorado para verificar permisos de área o rol
def area_and_rol_required(allowed_areas=[], allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("You are not authenticated.")
            
            # Verificar si el usuario tiene permisos de superusuario
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Verificar si el usuario pertenece a alguna de las áreas
            area_match = UserArea.objects.filter(
                user=request.user,
                area__name__in=allowed_areas
            ).exists() if allowed_areas else True  # Si no se pasa filtro de área, se considera válido

            # Verificar si el usuario tiene alguno de los roles, en esas mismas áreas
            role_match = UserRol.objects.filter(
                user=request.user,
                rol__name__in=allowed_roles,
                rol__area__name__in=allowed_roles
            ).exists() if allowed_roles else True  # Igual, si roles=[] se considera válido
            
            if not (area_match or role_match):
                messages.info(request, "No tienes los permisos requeridos.")
                return redirect(request.META.get("HTTP_REFERER", "/"))
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator