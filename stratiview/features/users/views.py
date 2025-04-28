from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from stratiview.models import User, State  # Asegúrate de que los imports estén correctos
from django.db import transaction
from stratiview.features.users.utils import send_credentials_email, generate_password, send_password_reset_email
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["GET"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["GET"]},
])
def users(request):
    if request.method == "GET":
        states  = State.objects.all()
        users = User.objects.select_related('state').only(
            "id", 
            "email", 
            "username", 
            "first_name", 
            "last_name",
            "phone", 
            "date_joined", 
            "is_active",
            "state"
        ).filter(is_superuser=False, is_active = True).order_by("-date_joined")

        return render(request, "users/users.html", {
            "users": users,
            "states": states,
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
            return redirect(reverse("users"))

        user = User.objects.select_related('state').only(
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "phone",
            "state",
        ).filter(id=user_id).first()
        if not user:
            return JsonResponse({})
        
        return JsonResponse({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "username": user.username,
            "phone": user.phone,
            "is_locked": user.is_locked,
            "state_id": user.state.id,
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
        # grupo_nombre = request.POST.get("grupo")  # opcional

        # Validar si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Ya existe un usuario con ese correo.")
            return redirect(reverse("users"))

        # Obtener el estado si fue proporcionado
        state_obj = None
        if state_id:
            try:
                state_obj = State.objects.get(id=state_id)
            except State.DoesNotExist:
                messages.error(request, "Entidad federativa inválida.")
                return redirect(reverse("users"))

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

                # Enviar correo electrónico al usuario
                if new_user:
                    try:
                        send_credentials_email(temp_password, first_name, last_name, email)
                    except Exception as e:
                        messages.info(request, f"Error al enviar el correo electrónico: {e}")
                        return redirect(reverse("users"))
                    
            messages.info(request, "Usuario creado exitosamente. Credenciales enviadas al correo.")
            return redirect(reverse("users"))
        except Exception as e:
            messages.error(request, f"Error al crear el usuario.", e)
            return redirect(reverse("users"))

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
                return redirect(reverse("users"))
            except Exception as e:
                messages.error(request, f"Error al desbloquear el usuario.", e)
                return redirect(reverse("users"))

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
                return redirect(reverse("users"))
            except Exception as e:
                messages.error(request, f"Error al enviar las nuevas credenciales", e)
                return redirect(reverse("users"))
            
            
        if action == "save":
            email = request.POST.get("email")
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone = request.POST.get("phone")
            state_id = request.POST.get("state")

            if email:
                # Validar si el correo ya está registrado
                if User.objects.exclude(id=user_id).filter(email=email).exists():
                    messages.warning(request, "Ya existe un usuario con ese correo")
                    return redirect(reverse("users"))
                
                user.email = email

            if username:
                # Validar si el nombre de usuario ya está registrado
                if User.objects.exclude(id=user_id).filter(username=username).exists():
                    messages.warning(request, "Ya existe un usuario con ese nombre de usuario")
                    return redirect(reverse("users"))
                
                user.username = username
            
            if first_name:
                user.first_name = first_name
            
            if last_name:
                user.last_name = last_name

            if phone:
                user.phone = phone

            if state_id:
                try:
                    state_obj = State.objects.get(id=state_id)
                except State.DoesNotExist:
                    messages.warning(request, "Entidad federativa inválida")
                    return redirect(reverse("users"))
                
                user.state = state_obj

            user.save()
            messages.info(request, "Usuario editado exitosamente")
            return redirect(reverse("users"))
        

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
            messages.error(request, "Usuario no encontrado")
            return redirect(reverse("users"))
        
        if user.is_superuser:
            messages.error(request, "No se puede eliminar un superusuario")
            return redirect(reverse("users"))
        
        try:
            with transaction.atomic():
                user.is_active = False
                user.save()
            messages.info(request, "Usuario eliminado exitosamente")
            return redirect(reverse("users"))
        except Exception as e:
            messages.error(request, f"Error al eliminar el usuario: {e}")
            return redirect(reverse("users"))