from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15)
    # is_active = models.BooleanField(default=False)  # Add is_active field


    def __str__(self):
        return self.username


    
