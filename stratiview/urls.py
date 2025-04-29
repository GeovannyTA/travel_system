from django.contrib import admin
from django.urls import path, include
from stratiview.features.viewer import views
from django.conf import settings
from django.conf.urls.static import static
from stratiview.features.utils import utils
from django.shortcuts import redirect

urlpatterns = [
    path('stratiview/', lambda request: redirect('/stratiview/viewer/')),
    path('stratiview/admin/', admin.site.urls),
    path('stratiview/viewer/', include('stratiview.features.viewer.urls')),
    path('stratiview/check_sesion/', utils.check_sesion, name='check_sesion'),
    path('stratiview/panoramas/', include('stratiview.features.panoramas.urls')),
    path('stratiview/auth/', include('stratiview.features.auth.urls')),
    path('stratiview/users/', include('stratiview.features.users.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)