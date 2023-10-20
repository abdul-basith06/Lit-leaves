from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    icon = models.ImageField(upload_to='images/category_icons/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    