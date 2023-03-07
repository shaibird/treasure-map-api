from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_pins')
    private = models.BooleanField(default=True)
    date = models. DateTimeField(auto_now_add=True)