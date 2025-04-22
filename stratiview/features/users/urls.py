from django.urls import path
from stratiview.features.users import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.users, name='users'),
    path('new_user/', login_required(views.add_user), name='add_user'),
]