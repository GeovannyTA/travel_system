from django.contrib import admin
from django.urls import path, include
from stratiview.features import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.home), name='home'),
    path('panoramas/', include('stratiview.features.panoramas.urls')),
    path('auth/', include('stratiview.features.auth.urls')),
    path('users/', include('stratiview.features.users.urls')),
]
