from django.urls import path
from stratiview.features.panoramas import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.get_panoramas), name='panoramas'),
    path('add_panoramas/', login_required(views.add_panoramas), name='add_panoramas'),
]