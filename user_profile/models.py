from django.db import models
from userauths.models import *
from PIL import Image


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='images/dp/', blank=True, null=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        if self.dp:
            img = Image.open(self.dp.path)
            if img.width > 150 or img.height > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.dp.path)
    