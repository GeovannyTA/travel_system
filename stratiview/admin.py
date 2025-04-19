from django.contrib import admin
from stratiview.models import PanoramaMetadata, State

@admin.register(PanoramaMetadata)
class PanoramaMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'gps_lat', 'gps_lng', 'gps_alt', 'gps_direction', 'orientation', 'camera_make', 'camera_model', 'software', 'date_taken', 'date_uploaded')
    search_fields = ('name', 'camera_make', 'camera_model')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)