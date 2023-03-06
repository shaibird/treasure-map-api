from django.db import models
from django.contrib.auth.models import User

class LayerName(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_layer")
    locations = models.ManyToManyField("Location", related_name="layers")