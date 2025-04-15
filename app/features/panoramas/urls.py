from django.urls import path
from app.features.panoramas import views

urlpatterns = [
    path('', views.get_panoramas, name='get_panoramas'),
    path('add_panoramas/', views.add_panoramas, name='add_panoramas'),
]