from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import render
from stratiview.models import UserArea, UserRol
from django.contrib import messages
from django.db.models.functions import Lower


# Decorado para verificar permisos de área o rol
def area_matrix(rules=None):
    """
    rules = [
        {"areas": ["soporte tecnico"], "methods": ["GET"]},
        {"areas": ["administracion"], "methods": ["GET", "POST"]},
    ]
    """
    rules = rules or []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("No autenticado.")

            method = request.method.upper()

            user_areas = set(
                UserArea.objects.filter(user=user)
                .annotate(lower_area=Lower("area__name"))
                .values_list("lower_area", flat=True)
            )

            if not user_areas:
                messages.info(request, "No tienes los permisos requeridos")
                return render(request, "viewer/viewer.html")

            for rule in rules:
                rule_areas = set(rule.get("areas", []))
                rule_methods = set([m.upper() for m in rule.get("methods", [])])

                area_match = not rule_areas or bool(user_areas.intersection(rule_areas))
                method_match = not rule_methods or method in rule_methods

                if area_match and method_match:
                    return view_func(request, *args, **kwargs)

            messages.info(request, "No tienes los permisos requeridos")
            return render(request, "viewer/viewer.html")
        


        return _wrapped_view

    return decorator


def role_matrix(rules=None):
    """
    rules = [
        {"roles": ["Administrador"], "methods": ["GET", "POST"]},
        {"roles": ["Supervisor"], "methods": ["GET"]},
    ]
    """
    rules = rules or []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("No autenticado")

            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            method = request.method.upper()

            user_roles = set(
                UserRol.objects.filter(user=user)
                .annotate(lower_rol=Lower("rol__name"))
                .values_list("lower_rol", flat=True)
            )

            for rule in rules:
                rule_roles = set(rule.get("roles", []))
                rule_methods = set([m.upper() for m in rule.get("methods", [])])

                role_match = not rule_roles or bool(user_roles.intersection(rule_roles))
                method_match = not rule_methods or method in rule_methods

                if role_match and method_match:
                    return view_func(request, *args, **kwargs)

            messages.info(request, "No tienes los permisos requeridos")
            return render(request, "viewer/viewer.html")

        return _wrapped_view

    return decorator