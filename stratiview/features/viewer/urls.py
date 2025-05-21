from django.urls import path
from stratiview.features.viewer import views


urlpatterns = [
    path('<int:route_id>/', views.viewer, name='viewer'),
    path('public/<int:route_id>/', views.viewer_public, name='viewer_public'),
    path('public/<str:gps_lat>/<str:gps_lng>/', views.viewer_coordenates, name='viewer_coordenates'),
    path('get_nodes/<int:route_id>/<int:node_id>/', views.get_nodes, name='get_nodes'),
    path('get_routes/', views.get_routes, name='get_routes'),
    path("aframe-tour/<int:route_id>/", views.aframe_tour, name="aframe_tour"),
    path("aframe-tour/<int:route_id>/<int:node_id>/", views.aframe_tour),
]