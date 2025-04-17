from django.db import models

class panorama_metadata(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, blank=False, null=False)
    url = models.CharField(max_length=400, blank=False, null=False)
    gps_lat = models.FloatField(blank=False, null=False)
    gps_lng = models.FloatField(blank=False, null=False)
    gps_alt = models.FloatField(blank=False, null=False)
    gps_direction = models.FloatField(blank=False, null=False)
    orientation = models.IntegerField(blank=False, null=False)
    camera_make = models.CharField(max_length=100, blank=False, null=False)
    camera_model = models.CharField(max_length=100, blank=False, null=False)
    software = models.CharField(max_length=100, blank=False, null=False)
    date_taken = models.DateTimeField(blank=False, null=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'panorama_metadata'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'gps_lat', 'gps_lng', 'gps_alt'], 
                name='unique_panorama_fields')
        ]

class state(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'state'