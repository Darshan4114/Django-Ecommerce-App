from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

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
    
    def get_remove_single_item_url(self):
        return reverse ("core:remove_single_item", args=[str(self.id)])
    

class OrderItem(models.Model):
    user = models.ForeignKey(user_model,on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    qty = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name

    def get_total_item_price(self):
        return (self.item.price * self.qty)
    
    def get_total_discount_item_price(self):
        return (self.item.disc_price * self.qty)

    def get_final_price(self):
        if self.item.disc_price:
            return (self.item.disc_price * self.qty)
        else:
            return (self.item.price * self.qty)

class Order(models.Model):
    user = models.ForeignKey(user_model,on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    billing_add = models.ForeignKey(
        'BillingAdd', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        return total

class BillingAdd(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    add1 = models.CharField(max_length=100)
    add2 = models.CharField(max_length=100)
    country = CountryField()
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username