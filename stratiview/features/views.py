from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stratiview.features.utils.permisions import area_and_rol_required
from stratiview.models import UserArea, UserRol, User

@login_required
@area_and_rol_required(allowed_areas=['desarrollo'], allowed_roles=['admin'])
def home(request):
    return render(request, 'home/home.html')