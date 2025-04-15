from django.contrib import admin
from app.models import panorama_metadata

@admin.register(panorama_metadata)
class PanoramaMetadataAdmin(admin.ModelAdmin):
    pass