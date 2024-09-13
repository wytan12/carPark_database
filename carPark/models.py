from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class CarParkInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    carpark_id = models.CharField(max_length=180)
    name = models.CharField(max_length=180)
    lot_type = models.CharField(max_length=5, default='C')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    total_capacity = models.IntegerField()
    agency = models.CharField(max_length=180)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'carpark_info'
        constraints = [
            models.UniqueConstraint(fields=['carpark_id', 'lot_type'], name='unique_carpark')
        ]


class CarParkAvailability(models.Model):
    info = models.ForeignKey(CarParkInfo, on_delete=models.CASCADE, to_field="id")
    # name = models.CharField(max_length=180)
    # lot_type = models.CharField(max_length=5, default='C')
    available_lot = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'carpark_availability'
