from django.db import models
from django.contrib.auth.models import User
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    username = models.CharField(max_length=25)
    location = models.CharField(max_length=30)
    birthday = models.DateField()
    photo_url = models.CharField(max_length=200)