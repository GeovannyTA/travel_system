from django.urls import path
from stratiview.features.markers import views


urlpatterns = [
    # Property marker
    path('add_marker/', views.add_marker, name='add_marker'),
    path('get_markers/', views.get_markers, name='get_markers'),
    # Router marker
    path('add_route_marker/', views.add_route_marker, name='add_route_marker'),
    path('get_route_markers/', views.get_route_markers, name='get_route_markers'),
    # Object marker
    path('add_object_marker/', views.add_object_marker, name='add_object_marker'),
    path('get_object_markers/', views.get_object_markers, name='get_object_markers'),
]