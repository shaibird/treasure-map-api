from django.db import models
from django.contrib.auth.models import User

class LayerPin(models.Model):
    layer = models.ForeignKey("LayerName", on_delete=models.CASCADE, related_name="layer_pins")
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="location_pins")