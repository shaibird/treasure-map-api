from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(null=True, blank=True, height_field=None,
                              width_field=None, max_length=None, upload_to="images")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="location_images")
    private = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)


