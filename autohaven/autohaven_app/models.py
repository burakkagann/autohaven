from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.

class SellerUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=255,blank=True,null=True)

  
class Listing(models.Model):
    NEW = 'new'
    USED = 'used'

    LISTING_TYPES = [
        (NEW, 'New Car'),
        (USED, 'Used Car'),
    ]

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255,default='')
    type=models.CharField(max_length=4, choices= LISTING_TYPES)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    brand= models.CharField(max_length=100)
    mileage = models.FloatField()
    engine_type = models.CharField(max_length=100)
    body_type = models.CharField(max_length=100,default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold = models.BooleanField(default=False)

class ListingImage(models.Model):
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    imagepath = models.ImageField(upload_to='listing_images/')

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offers')
    offeredPrice= models.DecimalField(max_digits=10, decimal_places=2)
    offeredDate= models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=100)
