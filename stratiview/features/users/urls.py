from django.urls import path
from stratiview.features.users import views


urlpatterns = [
    path('', views.users, name='users'),
    path('new_user/', views.add_user, name='add_user'),
]