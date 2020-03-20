from django.db import models
from django.conf import settings
from django.shortcuts import reverse

user_model = settings.AUTH_USER_MODEL

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    disc_price = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ("core:item_detail", args=[str(self.id)])
    
    def get_add_to_cart_url(self):
        return reverse ("core:add_to_cart", args=[str(self.id)])

    def get_remove_from_cart_url(self):
        return reverse ("core:remove_from_cart", args=[str(self.id)])

class OrderItem(models.Model):
    user = models.ForeignKey(user_model,on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    qty = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name

class Order(models.Model):
    user = models.ForeignKey(user_model,on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    
    def __str__(self):
        return self.user.username

    