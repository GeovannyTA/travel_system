from django.urls import path
from stratiview.features.states import views


urlpatterns = [
    path('', views.get_states, name='states'),
    path("add_state/", views.add_state, name="add_state"),
    path("get_state/<int:state_id>/", views.get_state, name="get_state")
]