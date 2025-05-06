from django.urls import path
from stratiview.features.routes import views


urlpatterns = [
    path('', views.get_routes, name='routes'),
    path("get_route/<int:route_id>/", views.get_route, name="get_route"),
    path("add_route/", views.add_route, name="add_route"),
    path("edit_route/", views.edit_route, name="edit_route"),
    path("delete_route/", views.delete_route, name="delete_route"),
]