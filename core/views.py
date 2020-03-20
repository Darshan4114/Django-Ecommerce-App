from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone

# Create your views here.

class item_list(ListView):
    model = Item

class item_detail(DetailView):
    model = Item
    
def add_to_cart(request, id):
    item = get_object_or_404(Item,id = id)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        #checking if item is in order
        if order.items.filter(item__id = id).exists():
            order_item = OrderItem.objects.filter(item__id = id)
            order_item = order_item[0]
            order_item.qty +=1
            order_item.save()
        
        #if order item's not in order
        else:
            order_item = OrderItem.objects.create(item = item, user = request.user)
            order.items.add(order_item)
            order_item.qty +=1
            order_item.save()
    else:
        ordered_date = timezone.now()
        order_item = OrderItem.objects.create(item = item)
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        order_item.qty +=1  
        order_item.save()

    

    return redirect("core:item_detail", pk=id)

def remove_from_cart(request, id):
    item = get_object_or_404(Item,id = id)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item = OrderItem.objects.filter(
                item__id = item.id,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            
        else:
            #Item is not in order
            print("Item not in order")
    else:
        #Order does not exist
        print("Order does not exist")

    return redirect("core:item_detail", pk=id)