from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stratiview.models import UserArea, UserRol, User

@login_required
def home(request):
    return render(request, 'home/home.html')