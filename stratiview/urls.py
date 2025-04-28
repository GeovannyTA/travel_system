from django.contrib import admin
from django.urls import path, include
from stratiview.features import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('stratiview/admin/', admin.site.urls),
    path('stratiview/', login_required(views.home), name='home'),
    path('stratiview/check_sesion/', views.check_sesion, name='check_sesion'),
    path('stratiview/panoramas/', include('stratiview.features.panoramas.urls')),
    path('stratiview/auth/', include('stratiview.features.auth.urls')),
    path('stratiview/users/', include('stratiview.features.users.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)