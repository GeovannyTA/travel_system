from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('stratiview', '0020_make_route_non_nullable'),
    ]

    operations = [
        # Volver a agregar la constraint en PanoramaTourMarkers
        migrations.AddConstraint(
            model_name='panoramatourmarkers',
            constraint=models.UniqueConstraint(
                fields=('yaw', 'pitch', 'panorama'),
                name='unique_panorama_tour_markers_fields'
            ),
        ),
        # Volver a agregar la constraint en UserRoute
        migrations.AddConstraint(
            model_name='userroute',
            constraint=models.UniqueConstraint(
                fields=('user', 'route'),
                name='unique_user_route_fields'
            ),
        ),
    ]
