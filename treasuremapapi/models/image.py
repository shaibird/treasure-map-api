from django.db import models
from django.contrib.auth.models import User
class Image(models.Model):
    url = models.URLField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="location_images")
    private = models.BooleanField(default=True)