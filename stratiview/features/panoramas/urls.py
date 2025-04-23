from django.urls import path
from stratiview.features.panoramas import views


urlpatterns = [
    path('', views.get_panoramas, name='panoramas'),
    path('add_panoramas/', views.add_panoramas, name='add_panoramas'),
    path("get_panorama/<int:panorama_id>/", views.get_panorama, name="get_panorama"),
    path("edit_panorama/", views.edit_panorama, name="edit_panorama"),
    path("delete_panorama/", views.delete_panorama, name="delete_panorama"),
]