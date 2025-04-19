from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group
from stratiview.models import User, State  # Asegúrate de que los imports estén correctos
from django.db import transaction

def registrar_usuario(request):
    if request.method == "GET":
        # Si es GET, mostrar formulario
        estados = State.objects.all()
        grupos = Group.objects.all()
        return render(request, "users/new_user.html", {
            "estados": estados,
            "grupos": grupos
        })

    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        username = request.POST.get("username").strip().lower()
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        phone = request.POST.get("phone").strip()
        state_id = request.POST.get("state")
        # grupo_nombre = request.POST.get("grupo")  # opcional

        # Validar si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return redirect("new_user")

        # Obtener el estado si fue proporcionado
        state_obj = None
        if state_id:
            try:
                state_obj = State.objects.get(id=state_id)
            except State.DoesNotExist:
                messages.error(request, "Entidad federativa inválida.")
                return redirect("new_user")

        # Generar una contraseña temporal
        temp_password = get_random_string(length=10)

        # Crear usuario
        try:
            with transaction.atomic():
                User.objects.create_user(
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
        except Exception as e:
            messages.error(request, f"Error al crear el usuario.", e)
        messages.success(request, f"Usuario creado exitosamente. Contraseña temporal: {temp_password}")
        return redirect("panoramas")
