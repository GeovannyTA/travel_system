from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('stratiview', '0019_populate_route_in_panoramatourmarkers'),
    ]

    operations = [
        # First, remove the existing constraint
        migrations.RemoveConstraint(
            model_name='panoramametadata',
            name='unique_panorama_fields',
        ),
        
        # Then make the fields non-nullable
        migrations.AlterField(
            model_name='panoramametadata',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stratiview.route'),
        ),
        migrations.AlterField(
            model_name='panoramatourmarkers',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stratiview.route'),
        ),
        migrations.AlterField(
            model_name='userroute',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stratiview.route'),
        ),
        
        # Finally, re-add the constraint
        migrations.AddConstraint(
            model_name='panoramametadata',
            constraint=models.UniqueConstraint(
                fields=['name', 'gps_lat', 'gps_lng', 'gps_alt', 'route'],
                name='unique_panorama_fields'
            ),
        ),
    ]
