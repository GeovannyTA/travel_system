from django.urls import path
from stratiview.features.markers import views


urlpatterns = [
    path('add_marker/', views.add_marker, name='add_marker'),
]