from django.urls import path
from stratiview.features.users import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path('', views.get_panoramas, name='panoramas'),
    path('new_user/', login_required(views.registrar_usuario), name='new_user'),
]