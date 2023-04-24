import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from paypalcheckoutsdk.orders import OrdersGetRequest

from accounts.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem
from payment.forms import PaymentForm

from .decorators import address_required, cart_required, delivery_required
from .models import DeliveryOptions
from .paypal import PayPalClient

# Create your views here.


@cart_required
@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(
        request,
        "checkout/delivery_choices.html",
        {"deliveryoptions": deliveryoptions},
    )


@cart_required
@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(
            delivery_type.delivery_price
        )
        session = request.session
        if "purchase" not in session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse(
            {
                "total": updated_total_price,
                "delivery_price": delivery_type.delivery_price,
            }
        )
        return response


@delivery_required
@cart_required
@login_required
def delivery_address(request):
    """ """
    session = request.session
    addresses = Address.objects.filter(customer=request.user).order_by(
        "-default"
    )

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True
    return render(
        request, "checkout/delivery_address.html", {"addresses": addresses}
    )


@address_required
@delivery_required
@cart_required
@login_required
def payment_selection(request):
    """"""
    form = PaymentForm()
    return render(request, "checkout/payment_selection.html", {"form": form})


@address_required
@delivery_required
@cart_required
@login_required
def payment_complete(request):
    """"""
    PPClient = PayPalClient()
    session = request.session

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[
            0
        ].shipping.address.address_line_1,
        address2=response.result.purchase_units[
            0
        ].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[
            0
        ].shipping.address.postal_code,
        country_code=response.result.purchase_units[
            0
        ].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key="LC" + response.result.id,
        payment_option="paypal",
        billing_status=True,
        delivery_method=DeliveryOptions.objects.get(
            id=session["purchase"]["delivery_id"]
        ).delivery_name,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(
            order_id=order_id,
            product=item["product"],
            price=item["price"],
            quantity=item["qty"],
        )

    return JsonResponse("Payment completed!", safe=False)
