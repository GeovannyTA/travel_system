from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages  # opcional para mostrar errores
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import re


User = get_user_model()
MAX_ATTEMPTS = 3

@never_cache
@csrf_protect
def sign_in(request):
    if request.session.pop('session_expired', False):
        messages.info(request, "Tu sesión ha expirado por inactividad.")

    if request.method == "GET":
        return render(request, "auth/sign_in.html")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Debes ingresar tu correo y contraseña.")
            return render(request, "auth/sign_in.html", context={"email": email})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if not user:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, "auth/sign_in.html", context={"email": email})

        # Bloqueado por administrador
        if user.is_locked:
            messages.warning(request, "Tu cuenta está bloqueada. Contacta al administrador.")
            return render(request, "auth/sign_in.html", context={"email": email})

        # Verificar si la cuenta está activa
        auth_user = authenticate(request, username=user.username, password=password)

        if not user.is_active:
            messages.warning(request, "Tu cuenta no está activa. Contacta al administrador.")
            return render(request, "auth/sign_in.html", context={"email": email})

        # Fallo de autenticación o cuenta inactiva
        if not auth_user:
            user.failed_attempts += 1
            if user.failed_attempts >= MAX_ATTEMPTS:
                user.is_locked = True
                messages.warning(request, "Demasiados intentos fallidos. Tu cuenta ha sido bloqueada.")
            else:
                restantes = MAX_ATTEMPTS - user.failed_attempts
                messages.error(
                    request,
                    f"Credenciales incorrectas. Intentos restantes: {restantes}",
                )

            # Guardar los intentos fallidos
            user.save()
            return render(request, "auth/sign_in.html", context={"email": email})

        # Si pasa esta parte, el login fue exitoso
        login(request, auth_user)
        user.failed_attempts = 0
        user.save()

        if user.must_change_password:
            return redirect("password_change")

        return redirect("routes")


@require_POST
@csrf_protect
@login_required
def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()

    try:
        return redirect(reverse("sign_in"))
    except NoReverseMatch:
        return redirect("/auth/sign_in/")


@login_required
def change_password_view(request):
    if request.method == "GET":
        if not request.user.must_change_password:
            return redirect(reverse("routes"))
        
        return render(request, "auth/password_change.html")

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not old_password or not new_password1 or not new_password2:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect("password_change")

        if new_password1 != new_password2:
            messages.error(request, "Las nuevas contraseñas no coinciden")
            return redirect("password_change")

        if not request.user.check_password(old_password):
            messages.error(request, "La contraseña actual es incorrecta")
            return redirect("password_change")

        # Validación de fuerza
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"
        if not re.match(regex, new_password1):
            messages.error(
                request, 
                "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un símbolo"
            )
            return redirect("password_change")

        # Todo correcto, guardar nueva contraseña
        request.user.set_password(new_password1)
        request.user.must_change_password = False
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect("routes")