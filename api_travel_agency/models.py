from django.db import models
from django.utils.timezone import now

    
class Location(models.Model):
    auto_increment_id = models.IntegerField(primary_key=True, blank=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    number = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    image_url = models.CharField(max_length=256, blank=True, null=True)
    
    
class Holiday(models.Model):
    auto_increment_id = models.IntegerField(primary_key=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, blank=True, null=True)
    start_date =  models.DateField(blank=True, default=now)
    duration = models.IntegerField(blank=True, null=True)
    price = models.CharField(max_length=256, blank=True, null=True)
    free_slots = models.IntegerField(blank=True, null=True)


class Reservation(models.Model):
    auto_increment_id = models.IntegerField(primary_key=True, blank=True)
    contact_name = models.CharField(max_length=256, blank=True, null=True)
    phone_number = models.CharField(max_length=256, blank=True, null=True)
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
