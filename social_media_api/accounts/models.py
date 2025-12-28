from django.db import models
from django.contrib.auth.models import AbstractUser
#creating custom user model, you are replacign default user 
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='following'
    )
