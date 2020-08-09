from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class CurrentBid(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    initial = models.BooleanField(default="True")

    def __str__(self):
        return f"${self.amount} by {self.user.username}"

class Listing(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    init_bid = models.IntegerField(default=0)
    currentbid = models.ForeignKey(CurrentBid, on_delete=models.CASCADE, blank=True, default=None, related_name="bids")
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    image = models.TextField(blank=True)
    category = models.ManyToManyField(Category, related_name='listing_category')
    active = models.BooleanField()

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_creator")
    datetime = models.DateField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user.username}"

class Watchlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")

    def __str__(self):
        return f"{self.user} watching {self.listing.title}"