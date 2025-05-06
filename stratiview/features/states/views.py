from django.shortcuts import render
from stratiview.models import State
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_matrix, role_matrix
from django.contrib import messages
from stratiview.features.utils.utils import soft_redirect
from django.urls import reverse
from django.http import JsonResponse


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["GET"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["GET"]},
])
def get_states(request):
    states = State.objects.all()
    return render(request, 'states/states.html', {'states': states})


"""

"""
def get_state(request, state_id):
    if request.method == "GET":
        # if request.headers.get("x-requested-with") != "XMLHttpRequest":
        #     return soft_redirect(reverse("users"))

        state = State.objects.only(
            'id', 
            'name', 
        ).filter(id=state_id).first()

        if not state:
            return JsonResponse({})
        
        return JsonResponse({
            "id": state.id,
            "name": state.name,
        })


@login_required
@area_matrix(rules=[
    {"areas": ["administracion"], "methods": ["POST"]},
])
@role_matrix(rules=[
    {"roles": ["administrador"], "methods": ["POST"]},
])
def add_state(request):
    name = request.POST.get('add-state-name')

    if not name:
        messages.warning(request, "El nombre es un dato obligatorio")
        return soft_redirect(reverse("states"))

    # Veficiar que el estado no se encuentre en la db
    state_exist = State.objects.filter(name=name).exists()
    if state_exist:
        messages.warning(request, "El estado ya se encuentra registrado")
        return soft_redirect(reverse("states"))

    try:
        State.objects.create(
            name = name
        )
    except Exception as e:
        messages.warning(request, "No se ha podido crear el estado")
        return soft_redirect(reverse("states"))
    
    messages.info(request, "El estado se ha creado exitosamente")
    return soft_redirect(reverse("states"))