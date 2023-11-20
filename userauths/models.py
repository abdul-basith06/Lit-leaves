import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15)
    # is_active = models.BooleanField(default=False)  # Add is_active field
    
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the user is being created (not updated)
        super().save(*args, **kwargs)

        if created:
            from user_profile.models import Wallet
            Wallet.objects.create(user=self, card_id=self.generate_card_id(), balance=0)

    def generate_card_id(self):
        # Generate a random 12-digit card ID using uuid
        card_id = str(uuid.uuid4().int)[:12]
        return card_id
   
            
    def __str__(self):
        return self.username


    
