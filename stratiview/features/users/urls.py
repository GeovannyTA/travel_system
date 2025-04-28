from django.urls import path
from stratiview.features.users import views


urlpatterns = [
    path('', views.users, name='users'),
    path('new_user/', views.add_user, name='add_user'),
    path("get_user/<int:user_id>/", views.get_user, name="get_user"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
]