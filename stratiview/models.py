from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'state'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    must_change_password = models.BooleanField(default=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'


class PanoramaMetadata(models.Model):
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
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'panorama_metadata'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'gps_lat', 'gps_lng', 'gps_alt', 'state'], 
                name='unique_panorama_fields')
        ]