from django.contrib import admin
from stratiview.models import User, PanoramaMetadata, UserArea, UserRol, Area, Rol, Route, UserRoute


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'area', 'description')
    search_fields = ('name', 'area__name')
    ordering = ('area', 'name')

@admin.register(UserArea)
class UserAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'area')
    search_fields = ('user__username', 'area__name')
    ordering = ('user', 'area')

@admin.register(UserRol)
class UserRolAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rol')
    search_fields = ('user__username', 'rol__name')
    ordering = ('user', 'rol')


@admin.register(PanoramaMetadata)
class PanoramaMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gps_lat', 'gps_lng', 'gps_alt', 'gps_direction', 'orientation', 'camera_make', 'upload_by', 'camera_model', 'software', 'date_taken', 'date_uploaded')
    search_fields = ('name', 'camera_make', 'camera_model', 'upload_by')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(UserRoute)
class UserRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'route')
    search_fields = ('user__username', 'route__name')
    ordering = ('user', 'route')