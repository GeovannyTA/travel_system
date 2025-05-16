from django.db import migrations

def forward_func(apps, schema_editor):
    PanoramaTourMarkers = apps.get_model('stratiview', 'PanoramaTourMarkers')
    for marker in PanoramaTourMarkers.objects.all():
        marker.route = marker.panorama.route
        marker.save()

def reverse_func(apps, schema_editor):
    PanoramaTourMarkers = apps.get_model('stratiview', 'PanoramaTourMarkers')
    PanoramaTourMarkers.objects.update(route=None)

class Migration(migrations.Migration):

    dependencies = [
        ('stratiview', '0018_add_nullable_route_to_panoramatourmarkers'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func),
    ]
