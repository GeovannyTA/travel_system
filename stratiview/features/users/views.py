from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.crypto import get_random_string
from stratiview.models import User, State  # Asegúrate de que los imports estén correctos
from django.db import transaction
from stratiview.features.users.utils import send_credentials_email
from django.contrib.auth.decorators import login_required

@login_required
def users(request):
    users = User.objects.filter(is_superuser=False).order_by("-date_joined")
    states  = State.objects.all()

    return render(request, "users/users.html", {
        "users": users,
        "states": states,
    })


@login_required
def add_user(request):
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
    temp_password = get_random_string(length=12)

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

