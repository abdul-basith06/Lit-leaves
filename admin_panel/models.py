from django.db import models
from PIL import Image
from django.urls import reverse

# Create your models here.
    
class Language(models.Model):
    name = models.CharField(max_length=50)    
    
    def __str__(self):
        return self.name
    
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
    price = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('shop:product', args=[str(self.id)])
    
    
    def __str__(self):
        return self.name
    

class ProductLanguageVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)  
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.language.name}"    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product_images/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.width > 750 or img.height > 750:
                output_size = (750, 750) 
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"{self.product.name} - {self.image.name}" if self.image else self.product.name

   