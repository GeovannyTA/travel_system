from django.urls import path
from stratiview.features.panoramas import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.get_panoramas), name='panoramas'),
    path('add_panoramas/', login_required(views.add_panoramas), name='add_panoramas'),
    path("get_panorama/<int:panorama_id>/", login_required(views.get_panorama), name="get_panorama"),
    path("edit_panorama/", login_required(views.edit_panorama), name="edit_panorama"),
    path("delete_panorama/", login_required(views.delete_panorama), name="delete_panorama"),
]