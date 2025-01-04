from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.email} registered as {self.username}"
    
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=140)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    url = models.URLField()
    category = models.CharField(max_length=64)
    bid_count = models.IntegerField()
    date = models.DateTimeField()
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listings')  # New field

    def __str__(self):
        return f"{self.user.username} created listing {self.title}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, default=None)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} raised to {self.amount}$"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)
    text = models.CharField(max_length=140)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} commented {self.text}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
    listings = models.ManyToManyField(Listing, blank=True, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username} has watchlisted {self.listings}"