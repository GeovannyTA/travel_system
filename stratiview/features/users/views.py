from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from stratiview.models import User, State, Area, Rol, UserArea, UserRol  # Asegúrate de que los imports estén correctos
from django.db import transaction
from stratiview.features.users.utils import send_credentials_email, generate_password, send_password_reset_email
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix
from stratiview.features.utils.utils import soft_redirect

@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["GET"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["GET"]},
])
def users(request):
    if request.method == "GET":
        # Obtner todos las entidades federativas        
        states  = State.objects.all().only(
            "id",
            "name",
        )
        # Obtner todas areas
        areas = Area.objects.all().only(
            "id",
            "name",
        )
        # Obtners todas los roles
        roles = Rol.objects.all().only(
            "id",
            "name",
            "area",
        )
        # Obtener todos los usuarios que no son superusuarios y están activos
        users = User.objects.select_related('state').only(
            "id", 
            "email", 
            "username", 
            "first_name", 
            "last_name",
            "phone", 
            "date_joined", 
            "is_active",
            "state",
        ).filter(is_superuser=False, is_active = True).order_by("-date_joined")

        return render(request, "users/users.html", {
            "users": users,
            "states": states,
            "areas": areas,
            "roles": roles,
        })


"""
No se implementan los decoradores de permisos para la siguiente funcion ya que 
se utiliza en el frontend para obtener los metadatos de la panorama y no se 
requiere permisos especiales para acceder a ella.
"""
@login_required
def get_user(request, user_id):
    if request.method == "GET":
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return soft_redirect(reverse("users"))

        user = User.objects.select_related('state').only(
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "phone",
            "is_locked",
            "is_active",
            "state",
        ).filter(id=user_id).first()
        if not user:
            return JsonResponse({})
        
        # Buscar el área y el rol asignado
        user_area = UserArea.objects.filter(user=user).first()
        user_rol = UserRol.objects.filter(user=user).first()
        
        return JsonResponse({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "username": user.username,
            "phone": user.phone,
            "is_locked": user.is_locked,
            "is_active": user.is_active,
            "state_id": user.state.id,
            "area_id": user_area.area.id,
            "rol_id": user_rol.rol.id,
        })


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def add_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        state_id = request.POST.get("state")
        area = request.POST.get("add-user-area")
        rol = request.POST.get("add-user-rol")

        if not email or not username or not first_name or not last_name or not phone or not state_id or not area or not rol:
            messages.warning(request, "Todos los campos son obligatorios.")
            return soft_redirect(reverse("users"))

        # Validar si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Ya existe un usuario con ese correo.")
            return soft_redirect(reverse("users"))

        # Obtener el estado si fue proporcionado
        state_obj = None
        if state_id:
            try:
                state_obj = State.objects.get(id=state_id)
            except State.DoesNotExist:
                messages.warning(request, "Entidad federativa inválida.")
                return soft_redirect(reverse("users"))

        # Generar una contraseña temporal
        temp_password = generate_password()

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    email = email,
                    username = username,
                    password = temp_password,
                    first_name = first_name,
                    last_name = last_name,
                    phone = phone,
                    state = state_obj,
                    must_change_password = True,
                    is_active = True,
                )

                UserArea.objects.create(
                    user = new_user,
                    area = Area.objects.get(id=area),
                )

                UserRol.objects.create(
                    user = new_user,
                    rol = Rol.objects.get(id=rol),
                )

                # Enviar correo electrónico al usuario
                if new_user:
                    try:
                        send_credentials_email(temp_password, first_name, last_name, email)
                    except Exception as e:
                        messages.info(request, f"Error al enviar el correo electrónico: {e}")
                        return redirect(reverse("users"))
                    
            messages.info(request, "Usuario creado exitosamente. Credenciales enviadas al correo.")
            return soft_redirect(reverse("users"))
        except Exception as e:
            messages.warning(request, f"Error al crear el usuario.", e)
            return soft_redirect(reverse("users"))

@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("edit-user-id")
        user = User.objects.get(id=user_id)

        action = request.POST.get("action")

        if action == "unlock":
            try:
                with transaction.atomic():
                    user.is_locked = False
                    user.failed_attempts = 0
                    user.save()
                messages.info(request, "Usuario desbloqueado exitosamente")
                return soft_redirect(reverse("users"))
            except Exception as e:
                messages.warning(request, f"Error al desbloquear el usuario.", e)
                return soft_redirect(reverse("users"))

        if action == "enable_user":
            try:
                with transaction.atomic():
                    user.is_active = True
                    user.save()
                messages.info(request, "Usuario habilitado exitosamente")
                return soft_redirect(reverse("users"))
            except Exception as e:
                messages.warning(request, f"Error al habilitar el usuario.", e)
                return soft_redirect(reverse("users"))

        if action == "reset_password":
            try:
                with transaction.atomic():
                    # Generar una nueva contraseña temporal
                    temp_password = generate_password()
                    user.is_locked = False
                    user.failed_attempts = 0
                    user.set_password(temp_password)
                    user.must_change_password = True
                    user.save()
                    send_password_reset_email(temp_password, user.first_name, user.last_name, user.email)
                messages.info(request, "Credenciales nuevas enviadas al correo")
                return soft_redirect(reverse("users"))
            except Exception as e:
                messages.warning(request, f"Error al enviar las nuevas credenciales", e)
                return soft_redirect(reverse("users"))
            
            
        if action == "save":
            fields = {
                "email": request.POST.get("edit-user-email"),
                "username": request.POST.get("edit-user-username"),
                "first_name": request.POST.get("edit-user-first_name"),
                "last_name": request.POST.get("edit-user-last_name"),
                "phone": request.POST.get("edit-user-phone"),
                "state_id": request.POST.get("edit-user-state"),
                "area_id": request.POST.get("edit-user-area"),
                "rol_id": request.POST.get("edit-user-rol"),
            }

            # Validar email duplicado
            if fields["email"] and User.objects.exclude(id=user_id).filter(email=fields["email"]).exists():
                messages.warning(request, "Ya existe un usuario con ese correo")
                return soft_redirect(reverse("users"))
            
            # Validar username duplicado
            if fields["username"] and User.objects.exclude(id=user_id).filter(username=fields["username"]).exists():
                messages.warning(request, "Ya existe un usuario con ese nombre de usuario")
                return soft_redirect(reverse("users"))

            # Asignar campos básicos
            for attr in ["email", "username", "first_name", "last_name", "phone"]:
                value = fields[attr]
                if value:
                    setattr(user, attr, value)

            # Actualizar estado (entidad federativa)
            if fields["state_id"]:
                try:
                    state_obj = State.objects.get(id=fields["state_id"])
                    user.state = state_obj
                except State.DoesNotExist:
                    messages.warning(request, "Entidad federativa inválida")
                    return soft_redirect(reverse("users"))

            # Actualizar área del usuario
            if fields["area_id"]:
                area_obj = Area.objects.filter(id=fields["area_id"]).first()
                if not area_obj:
                    messages.warning(request, "Área seleccionada no válida")
                    return soft_redirect(reverse("users"))

                user_area, _ = UserArea.objects.get_or_create(user=user)
                user_area.area = area_obj
                user_area.save()

            # Actualizar rol del usuario
            if fields["rol_id"]:
                rol_obj = Rol.objects.filter(id=fields["rol_id"]).first()
                if not rol_obj:
                    messages.warning(request, "Rol seleccionado no válido")
                    return soft_redirect(reverse("users"))

                user_rol, _ = UserRol.objects.get_or_create(user=user)
                user_rol.rol = rol_obj
                user_rol.save()

            user.save()
            messages.info(request, "Usuario editado exitosamente")
            return soft_redirect(reverse("users"))
        

@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("delete-user-id")
        user = User.objects.get(id=user_id)

        if not user:
            messages.warning(request, "Usuario no encontrado")
            return soft_redirect(reverse("users"))
        
        if user.is_superuser:
            messages.warning(request, "No se puede eliminar un superusuario")
            return soft_redirect(reverse("users"))
        
        try:
            with transaction.atomic():
                user.is_active = False
                user.save()
            messages.info(request, "Usuario eliminado exitosamente")
            return soft_redirect(reverse("users"))
        except Exception as e:
            messages.warning(request, f"Error al eliminar el usuario: {e}")
            return soft_redirect(reverse("users"))