from django.shortcuts import render
from stratiview.models import Route, UserArea, UserRol, UserRoute
from stratiview.features.utils.utils import soft_redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix


@login_required
@area_matrix(rules=[
    {"areas": ["administracion", "visualizacion"], "methods": ["GET"]},
])
@role_matrix(rules=[
    {"roles": ["administrador", "visor"], "methods": ["GET"]},
])
def get_routes(request):
    if request.method == "GET":
        # Verificar si el usuario tiene acceso a la ruta
        user_areas = set(
            UserArea.objects.filter(user=request.user)
            .annotate(lower_area=Lower("area__name"))
            .values_list("lower_area", flat=True)
        )
        user_roles = set(
            UserRol.objects.filter(user=request.user)
            .annotate(lower_rol=Lower("rol__name"))
            .values_list("lower_rol", flat=True)
        )

        if any(area in ["administracion"] for area in user_areas) or any(role in ["administrador"] for role in user_roles):
            routes = Route.objects.all()
        else:
            routes = Route.objects.filter(
                id__in= UserRoute.objects.filter(user=request.user).values_list("route_id", flat=True),
            ).filter(is_deleted=False)
        
        # Filtros
        route_name = request.GET.get("route_name")
        filter_is_deleted = request.GET.get("filter_is_deleted")
        
        if filter_is_deleted in ["True", "False"]:
            routes = routes.filter(is_deleted=(filter_is_deleted == "True"))

        if route_name:
            routes = routes.filter(name__icontains=route_name)

        # Paginación
        routes = routes.order_by("id")
        paginator = Paginator(routes, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'routes': page_obj,
            'route_name': route_name,
            'paginator': paginator,
        }
        return render(request, 'routes/routes.html', context)

"""
No se implementan los decoradores de permisos para la siguiente funcion ya que 
se utiliza en el frontend para obtener los metadatos de la panorama y no se 
requiere permisos especiales para acceder a ella.
"""
@login_required
def get_route(request, route_id):
    if request.method == "GET":
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return soft_redirect(reverse("users"))

        route = Route.objects.only(
            'id', 
            'name', 
            'description', 
            'is_deleted',
        ).filter(id=route_id).first()
        if not route:
            return JsonResponse({})
        
        return JsonResponse({
            "id": route.id,
            "name": route.name,
            "description": route.description,
            "is_deleted": route.is_deleted,
        })
    

@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def add_route(request):
    if request.method == "POST":
        name = request.POST.get("add-route-name")
        description = request.POST.get("add-route-description")

        if not name or not description:
            messages.warning(request, "Todos los campos son obligatorios")
            return soft_redirect(reverse("routes"))

        
        route_exist = Route.objects.filter(name=name).exists()
        if route_exist:
            messages.warning(request, "Ya existe un recorrido con ese nombre y estado")
            return soft_redirect(reverse("routes"))

        try:
            Route.objects.create(
                name=name,
                description=description,
            )
        except Exception as e:
            messages.warning(request, f"Error al crear el recorrido: {e}")
            return soft_redirect(reverse("routes"))
        
        messages.info(request, "Recorrido creado exitosamente")
        return soft_redirect(reverse("routes"))


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def edit_route(request):
    if request.method == "POST":
        route_id = request.POST.get("edit-route-id")
        action = request.POST.get("action")

        route = Route.objects.filter(id=route_id).first()
        if not route:
            messages.warning(request, "Recorrido no encontrado")
            return soft_redirect(reverse("routes"))
        
        if action == "enable":
            route.is_deleted = False
            route.save()
            messages.info(request, "Recorrido habilitado exitosamente")
            return soft_redirect(reverse("routes"))

        if action == "save":
            name = request.POST.get("edit-route-name")
            description = request.POST.get("edit-route-description")

            if name:
                route.name = name

            if description:
                route.description = description
            
            route.save()
            messages.info(request, "Recorrido editado exitosamente")
            return soft_redirect(reverse("routes"))


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def delete_route(request):
    if request.method == "POST":
        route_id = request.POST.get("delete-route-id")
        route = Route.objects.filter(id=route_id).first()

        if not route:
            messages.warning(request, "Recorrido no encontrado")
            return soft_redirect(reverse("routes"))
        
        route.is_deleted = True
        route.save()
        messages.info(request, "Recorrido eliminado exitosamente")
        return soft_redirect(reverse('routes'))