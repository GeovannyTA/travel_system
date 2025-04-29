from django.urls import path
from stratiview.features.viewer import views


urlpatterns = [
    path('', views.viewer, name='home'),
    path('get_nodes/', views.get_nodes, name='get_nodes'),
]