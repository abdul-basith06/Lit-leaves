from django.utils import timezone
from django.db import models
from admin_panel.models import *
from user_profile.models import *
from userauths.models import User
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_till = models.DateTimeField()
    discount_amount = models.PositiveIntegerField()
    min_purchase_amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    used_by = models.ManyToManyField(User, blank=True)  # Many-to-many relationship with users who have used the coupon

    def __str__(self):
        return self.code

    def is_user_eligible(self, user):
        """
        Check if a user is eligible to use the coupon.
        """
        return user not in self.used_by.all() 

    def mark_as_used(self, user):
        """
        Mark the coupon as used by a specific user.
        """
        self.used_by.add(user)
        self.save()    
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('RAZ', 'Paid With Razorpay'),
        ('WAL', 'Paid With Wallet'),       
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES,  null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    order_notes = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    applied_coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
 
   
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        
        if self.applied_coupon:
           if total >= self.applied_coupon.min_purchase_amount:
               return total - self.applied_coupon.discount_amount
        
        return total
    
    @property
    def get_cart_items(self):    
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)    
    variation = models.ForeignKey(ProductLanguageVariation, on_delete=models.SET_NULL, null=True, blank=True, related_name='variation') 
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True) 
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    ORDER_STATUS_CHOICES = [
        ('PL', 'Order placed'),
        ('DS', 'Dispatched'),
        ('SH', 'Shipped'),
        ('OFD', 'Out for Delivery'),
        ('D', 'Delivered'),
        ('CN', 'Order Cancelled'),
        ('RT', 'Returned'),
    ]
    
    delivery_status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default='PL')

    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total    
    

    

    