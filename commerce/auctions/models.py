from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='auctions/listings')
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="user_comments")
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=1, related_name="listing_comments")
    date = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.TextField(max_length=200, blank=True)
