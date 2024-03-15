from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    catogory_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.catogory_name


class Listings(models.Model):
    list_title = models.CharField(max_length=30)
    list_description = models.CharField(max_length=300)
    list_starting_bid = models.FloatField()
    list_image = models.CharField(max_length=1000)
    list_catagpry = models.ForeignKey(Category , on_delete=models.CASCADE)
    list_active = models.BooleanField(True)

    def __str__(self):
        return self.list_title