# Generated by Django 4.2.11 on 2025-06-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stratiview', '0025_implementta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='type',
            field=models.CharField(choices=[('Vehiculo', 'En vehículo'), ('Aereo', 'Aéreo'), ('Interior', 'Interior'), ('A pie', 'A pie')], default='Vehiculo', max_length=100),
        ),
    ]
