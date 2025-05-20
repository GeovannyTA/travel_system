from django.urls import path
from stratiview.features.viewer import views


urlpatterns = [
    path('<int:route_id>/', views.viewer, name='viewer'),
    path('public/<int:route_id>/', views.viewer_public, name='viewer_public'),
    path('public/<str:lat>/<str:lng>/', views.viewer_public, name='viewer_public'),
    path('get_nodes/<int:route_id>/', views.get_nodes, name='get_nodes'),
    path('get_routes/', views.get_routes, name='get_routes'),
]