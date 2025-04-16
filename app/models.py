from django.db import models

class panorama_metadata(models.Model):
    id = models.AutoField(primary_key=True)
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