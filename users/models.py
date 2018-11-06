from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    points = models.PositiveIntegerField(default=0)
    people = models.PositiveIntegerField(default=0)
    dworcowa3 = models.BooleanField(default=0)
    dworcowa10 = models.BooleanField(default=0)
    dworcowa13 = models.BooleanField(default=0)
    usedpoints = models.TextField(default='xdddddd')

    def __str__(self):
        return f'{self.user.username} Profile'
