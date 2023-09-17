from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    imageUrl = models.URLField(blank=True)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now)
    
    
class Bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now())
    
class Comments(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    datetime = models.DateTimeField(default=datetime.now())
    
class WatchList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now())