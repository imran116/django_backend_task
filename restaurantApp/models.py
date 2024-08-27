from django.db import models
from django.contrib.auth.models import User
from registerApp.models import Profile


# Create your models here.

class Restaurant(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='restaurants')
    restaurant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.restaurant_name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    menu_name = models.CharField(max_length=50)
    menu_desc = models.TextField()

    def __str__(self):
        return self.menu_name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menuItems')
    menu_items_name = models.CharField(max_length=100)
    menu_items_desc = models.TextField()
    menu_items_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.menu_items_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=100)
    menu_item_name = models.CharField(max_length=100)
    menu_item_desc = models.TextField()
    menu_item_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Name: {self.user.username}------Order price:{self.menu_item_price}"
