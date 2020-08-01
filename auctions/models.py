from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    bid = models.IntegerField()
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listingcreator")
    image = models.CharField(max_length=250, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name='Listing_category')
    active = models.BooleanField()

    def __str__(self):
        return f"{title}"

class Bids(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{bid} on {item} by {user.username}"

class Comments(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comment_creator")
    datetime = models.DateField(auto_now=True)

    def __str__(self):
        return f"Comment on {listing.title} by {user.username}"