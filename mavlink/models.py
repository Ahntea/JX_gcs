from django.db import models

class Drone(models.Model):
    status = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    battery_level = models.DecimalField(max_digits=4, decimal_places=2)
