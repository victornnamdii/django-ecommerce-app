from os import getenv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from rave_python import Misc, Rave, RaveExceptions
from rave_python.rave_misc import generateTransactionReference

from accounts.models import Address, Customer
from basket.basket import Basket
from basket.context_processors import product_list2
from checkout.models import DeliveryOptions
from orders.models import Order
from orders.views import order_add

from .decorators import cart_required, delivery_required
from .forms import PaymentForm

# Create your views here.
publicKey = getenv("RAVE_PUBLIC_KEY")
secretKey = getenv("RAVE_SECRET_KEY")
encKey = getenv("RAVE_ENC_KEY")

if secretKey:
    rave = Rave(publicKey, secretKey)
else:
    rave = Rave(
        "no_publicKey_available", "no_secretKey_available", usingEnv=False
    )


@delivery_required
@cart_required
@login_required
def BasketView(request):
    basket = Basket(request)

    user = Customer.objects.get(name=request.user)

    if request.method == "POST":
        if request.POST.get("step") == "cardcheck":
            session = request.session
            form = PaymentForm(request.POST)
            address = Address.objects.get(
                customer=user.id, pk=session["address"]["address_id"]
            )
            if form.is_valid():
                txRef = generateTransactionReference("LC" + str(user.id))
                payload = {
                    "cardno": form.cleaned_data["cardno"],
                    "cvv": form.cleaned_data["cvv"],
                    "currency": "NGN",
                    "country": "NG",
                    "expirymonth": form.cleaned_data["expirymonth"],
                    "expiryyear": form.cleaned_data["expiryyear"],
                    "amount": basket.get_total_price(),
                    "email": user.email,
                    "phonenumber": address.phone,
                    "txRef": txRef,
                    "enckey": encKey,
                }
                order_details = {
                    "full_name": address.full_name,
                    "address1": address.address_line,
                    "address2": address.address_line2,
                    "city": address.town_city,
                    "phone": address.phone,
                    "post_code": address.postcode,
                    "order_key": txRef,
                    "userid": str(user.id),
                    "cardno": str(form.cleaned_data["cardno"])[-4:],
                    "amount": basket.get_total_price(),
                    "email": user.email,
                    "option": "Card",
                    "delivery": DeliveryOptions.objects.get(
                        id=session["purchase"]["delivery_id"]
                    ).delivery_name,
                }
                order_items = []
                for item in product_list2(request)["product_list2"]:
                    item_dict = {}
                    item_dict["product"] = item[0]
                    item_dict["price"] = item[0].price
                    item_dict["qty"] = item[1]
                    order_items.append(item_dict)

                order_add(order_details, order_items)
                request.session["payload"] = payload
        try:
            payload = request.session["payload"]
            res = rave.Card.charge(payload)

            if res["suggestedAuth"]:
                arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

                if arg == "pin":
                    if request.POST.get("step") != "pincheck":
                        return render(request, "payment/verification/pin.html")
                    elif request.POST.get("step") == "pincheck":
                        pin = str(request.POST.get("first"))
                        pin += str(request.POST.get("second"))
                        pin += str(request.POST.get("third"))
                        pin += str(request.POST.get("fourth"))
                        Misc.updatePayload(
                            res["suggestedAuth"], payload, pin=pin
                        )
                        res = rave.Card.charge(payload)
                        request.session["payload"] = payload

            if res["validationRequired"]:
                if request.POST.get("step") != "otpcheck":
                    return render(request, "payment/verification/otp.html")
                if request.POST.get("step") == "otpcheck":
                    otp = str(request.POST.get("first"))
                    otp += str(request.POST.get("second"))
                    otp += str(request.POST.get("third"))
                    otp += str(request.POST.get("fourth"))
                    otp += str(request.POST.get("fifth"))
                    rave.Card.validate(res["flwRef"], otp)

            res = rave.Card.verify(res["txRef"])
            if res["transactionComplete"]:
                Order.objects.filter(order_key=payload["txRef"]).update(
                    billing_status=True
                )
                del request.session["payload"]
                return orderplaced(request)
            else:
                del request.session["payload"]
                messages.success(
                    request,
                    "There was a problem with your card. Check your details and try again",
                )
                return HttpResponseRedirect(
                    reverse("checkout:payment_selection")
                )

        except (
            RaveExceptions.CardChargeError,
            RaveExceptions.TransactionVerificationError,
            RaveExceptions.TransactionValidationError,
        ) as e:
            del request.session["payload"]
            messages.success(
                request,
                "There was a problem with your card. Check your details and try again",
            )
            return HttpResponseRedirect(reverse("checkout:payment_selection"))


def orderplaced(request):
    for item in product_list2(request)["product_list2"]:
        product = item[0]
        product.quantity = product.quantity - item[1]
        product.save()
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/orderplaced.html")
