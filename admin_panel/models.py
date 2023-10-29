from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    icon = models.ImageField(upload_to='images/category_icons/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=100, default='basi')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product_images/', blank=True, null=True)

    def __str__(self):
        return self.image.url


   