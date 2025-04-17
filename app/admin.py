from django.contrib import admin
from app.models import panorama_metadata, state

@admin.register(panorama_metadata)
class PanoramaMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'gps_lat', 'gps_lng', 'gps_alt', 'gps_direction', 'orientation', 'camera_make', 'camera_model', 'software', 'date_taken', 'date_uploaded')
    search_fields = ('name', 'camera_make', 'camera_model')

@admin.register(state)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)