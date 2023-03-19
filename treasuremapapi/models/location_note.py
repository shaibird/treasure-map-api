from django.db import models
from django.contrib.auth.models import User
class LocationNote(models.Model):
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="location_notes")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_locations')
    note = models.CharField(max_length=(1000))
    private = models.BooleanField(default=True) 
    date = models.DateTimeField(auto_now_add=True)
