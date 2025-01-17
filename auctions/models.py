from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=50)

class Listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=True) 
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids") 
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    bid_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

