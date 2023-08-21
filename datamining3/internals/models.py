from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
# Create your models here.

class ZipCode(models.Model):
    class Meta:
        unique_together = (('country','zip_code'),)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    
    #def get_absolute_url(self):
    #    return reverse("internals:zip-code-detail", kwargs={'id': self.id})
    
    def __str__(self):
        return str(self.id) + ":" + self.country + ":" + self.zip_code
    

class Attraction(models.Model):
    class Meta:
        unique_together = ('zip_code', 'place_id')

    zip_code = models.ForeignKey('ZipCode', on_delete=models.CASCADE)
    is_park = models.BooleanField()
    is_tourist_attraction = models.BooleanField()
    is_point_of_interest = models.BooleanField()
    is_establishment = models.BooleanField()
    place_id = models.CharField(max_length=100, null=False)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    data = models.CharField(max_length=10000, null=True, blank=True)
    rating = models.IntegerField()
    number_of_ratings = models.IntegerField()
    name = models.CharField(max_length=100, null=False)
    vicinity = models.CharField(max_length=100, null=False)
    photo_reference = models.CharField(max_length=100, blank=True)
