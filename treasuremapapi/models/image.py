from django.db import models
from django.contrib.auth.models import User

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Image(models.Model):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="location_images")
    private = models.BooleanField(default=True)