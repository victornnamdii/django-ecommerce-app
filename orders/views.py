from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem

# Create your views here.


def order_add(order_details, order_items):
    user_id = order_details["userid"]
    order_key = order_details["order_key"]
    baskettotal = order_details["amount"]

    if Order.objects.filter(order_key=order_key).exists():
        pass
    else:
        order = Order.objects.create(
            user_id=user_id,
            full_name=order_details["full_name"],
            address1=order_details["address1"],
            address2=order_details["address2"],
            city=order_details["city"],
            total_paid=baskettotal,
            order_key=order_key,
            phone=order_details["phone"],
            postal_code=order_details["post_code"],
            cardno=order_details["cardno"],
            email=order_details["email"],
            payment_option=order_details["option"],
            delivery_method=order_details["delivery"],
            country_code=order_details["country"],
            state=order_details["state"],
        )
        order_id = order.pk
        for item in order_items:
            OrderItem.objects.create(
                order_id=order_id,
                product=item["product"],
                price=item["price"],
                quantity=item["qty"],
            )


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
