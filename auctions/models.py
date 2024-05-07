from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Products(models.Model):
    title = models.CharField(max_length=64, default="Unnamed Product")
    description = models.TextField(default="No description available")
    initialprice = models.IntegerField(default=0)
    creatoruser = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='products')
    imageurl = models.URLField(null=True)
    datetime = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null='True', related_name='Products')

    def __str__(self):
        return f"{self.title}: {self.description} with price {self.initialprice} and user {self.creatoruser}"


class Bid(models.Model):
    price = models.IntegerField(default=0)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, related_name='productbids')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='userbids')

    def __str__(self):
        return f"{self.price} for {self.product}"


class Comment(models.Model):
    pass
