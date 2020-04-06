from django.urls import path
from .views import item_list, item_detail, add_to_cart, remove_from_cart, order_summary, remove_single_item, checkout, payment
app_name='core'

urlpatterns=[
    path('', item_list.as_view(), name='item_list'),
    path('detail/<int:pk>', item_detail.as_view(), name='item_detail'),
    path('add_to_cart/<int:id>', add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:id>', remove_from_cart, name = 'remove_from_cart'),
    path('order_summary', order_summary.as_view(), name='order_summary'),
    path('remove_single_item/<int:id>', remove_single_item, name = 'remove_single_item'),
    path('checkout', checkout.as_view(), name = 'checkout'),
    path('payment/<payment_option>', payment.as_view(), name = 'payment'),
]