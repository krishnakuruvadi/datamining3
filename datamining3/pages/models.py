from django.db import models
from internals.models import Attraction
from django.conf import settings

# Create your models here.


class UserRatings(models.Model):
    class Meta:
        unique_together = ('attraction', 'user')
    attraction = models.ForeignKey('internals.Attraction', on_delete=models.CASCADE)
    rating = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class UserRecommendations(models.Model):
    class Meta:
        unique_together = ('attraction', 'user')
    attraction = models.ForeignKey('internals.Attraction', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

