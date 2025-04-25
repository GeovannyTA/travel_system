from django.urls import path
from stratiview.features.auth import views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path("password_change/", views.change_password_view, name="password_change"),
]