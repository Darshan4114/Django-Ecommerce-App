from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Item, OrderItem, Order
from .forms import CheckoutForm
from django.views.generic import ListView, DetailView, View
from django.utils import timezone

# Create your views here.

class item_list(ListView):
    model = Item
    paginate_by = 10

class item_detail(DetailView):
    model = Item


class order_summary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order,
            }
            return render(self.request, 'order_detail.html', context)

        except ObjectDoesNotExist:
            messages.error('You do not have an active order')
            return redirect('/')
        
        
        
@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.qty += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order_summary")

@login_required
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
            messages.info(request,'Item removed from cart')

        else:
            messages.info(request,'Item not in cart')
            print("Item not in order")
    else:
        messages.info(request,'Order does not exist')
        print("Order does not exist")

    return redirect("core:order_summary")


@login_required
def remove_single_item(request, id):
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
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
                messages.info(request,'Item quantity reduced by 1')
            else:
                order.items.remove(order_item)
                order.save()
                order_item.delete()
                messages.info(request,'Item removed from cart')
            

        else:
            messages.info(request,'Item not in cart')
            print("Item not in order")
    else:
        messages.info(request,'Order does not exist')
        print("Order does not exist")

    return redirect("core:order_summary")


class checkout(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context={
            'form': form,
        }
        return render(self.request, 'checkout.html', context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            return redirect('core:checkout')
