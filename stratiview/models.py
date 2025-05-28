from django.db import models
from django.contrib.auth.models import AbstractUser


class Route(models.Model):
    TYPE_ROUTE = (
        ('vehicle', 'En vehículo'),
        ('air', 'Aéreo'),
        ('inside', 'Interior'),
        ('walk', 'A pie')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=False, null=False, choices=TYPE_ROUTE, default='vehicle')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'route'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    must_change_password = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)    

    @property
    def area_names(self):
        return list(self.userarea_set.values_list('area__name', flat=True))

    @property
    def rol_names(self):
        return list(self.userrol_set.values_list('rol__name', flat=True))
    
    class Meta:
        db_table = 'user'


class UserRoute(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'user_route'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'route'], 
                name='unique_user_route_fields')
        ]


class PanoramaMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, blank=False, null=False)
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
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False)
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)


    class Meta:
        db_table = 'panorama_metadata'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'gps_lat', 'gps_lng', 'gps_alt', 'route'], 
                name='unique_panorama_fields'
            ),
            models.UniqueConstraint(
                fields=['route'],
                condition=models.Q(is_default=True),
                name='unique_default_panorama_per_route'
            )
        ]
        

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'name'
    
    class Meta:
        db_table = 'area'


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=False, null=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'rol'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'area'], 
                name='unique_rol_fields')
        ]

class UserArea(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'user_area'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'area'], 
                name='unique_user_area_fields')
        ]

class UserRol(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'user_rol'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'rol'], 
                name='unique_user_rol_fields')
        ]     


class PanoramaPropertyMakers(models.Model):
    USE_CHOICES = [
        ('Comercial', 'Comercial'),
        ('Industrial', 'Industrial'),
        ('Equipamiento', 'Equipamiento'),
        ('Mixto', 'Mixto'),
        ('Residencial', 'Residencial'),
    ]

    SIZE_CHOICES = [
        ('Pequeño', 'pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]

    POSITION_CHOICES = [
        ('Esquinero', 'esquinero'),
        ('Intermedio', 'Intermerdio'),
        ('Manzanero', 'Manzanero'),
        ('Frentes no contiguos', 'Frentes no contiguis'),
        ('Paso de servicio', 'Paso de servicioo'),
    ]

    id = models.AutoField(primary_key=True)
    yaw = models.FloatField()
    pitch = models.FloatField()
    panorama = models.ForeignKey(PanoramaMetadata, on_delete=models.CASCADE)

    updated_use = models.CharField(max_length=50, choices=USE_CHOICES, default='residencial')
    property_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, default='mediano', blank=True, null=True)
    business_name = models.CharField(max_length=150, blank=True, null=True)
    land_position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='intermedio', blank=True, null=True)
    observation = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'panorama_property_markers'  

class PanoramaTourMarkers(models.Model):
    TYPE_MARKER = (
        ('vehiculo', 'Vehiculo'),
        ('aereo', 'Aereo'),
        ('interior', 'Interior'),
        ('a pie', 'A pie')
    )
    id = models.AutoField(primary_key=True)
    yaw = models.FloatField(blank=False, null=False)
    pitch = models.FloatField(blank=False, null=False)
    panorama = models.ForeignKey(PanoramaMetadata, on_delete=models.CASCADE, blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False, choices=TYPE_MARKER, default='vehiculo')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'panorama_tour_markers'
        constraints = [
            models.UniqueConstraint(
                fields=['yaw', 'pitch', 'panorama'], 
                name='unique_panorama_tour_markers_fields')
        ]


class PanoramaObjectMarkers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    yaw = models.FloatField(blank=False, null=False)
    pitch = models.FloatField(blank=False, null=False)
    panorama = models.ForeignKey(PanoramaMetadata, on_delete=models.CASCADE, blank=False, null=False)
    description = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        db_table = 'panorama_object_markers'
        constraints = [
            models.UniqueConstraint(
                fields=['yaw', 'pitch', 'panorama'], 
                name='unique_panorama_object_markers_fields')
        ]


class Implementta(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100, blank=False, null=False)
    gps_lat = models.FloatField(blank=False, null=False)
    gps_lng = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = 'implementta'