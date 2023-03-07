from django.db import models
from django.contrib.auth.models import User
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    bio = models.CharField(max_length=30)
    birthday = models.DateField()
    photo_url = models.URLField(max_length=800)