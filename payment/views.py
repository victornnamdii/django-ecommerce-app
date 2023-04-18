from os import getenv

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rave_python import Misc, Rave, RaveExceptions
from rave_python.rave_misc import generateTransactionReference

from accounts.models import UserBase
from basket.basket import Basket
from basket.context_processors import product_list2
from orders.models import Order
from orders.views import order_add

from .decorators import cart_required
from .forms import PaymentForm

# Create your views here.
publicKey = getenv("RAVE_PUBLIC_KEY", "")
secretKey = getenv("RAVE_SECRET_KEY", "")
encKey = getenv("RAVE_ENC_KEY", "")

rave = Rave(publicKey, secretKey)


@login_required
@cart_required
def BasketView(request):
    basket = Basket(request)

    user = UserBase.objects.get(user_name=request.user)

    if request.method != "POST":
        if request.session.get("payload"):
            del request.session["payload"]
        form = PaymentForm()
        return render(request, "payment/payment_form.html", {"form": form})

    if request.method == "POST":
        if request.POST.get("step") == "cardcheck":
            form = PaymentForm(request.POST)
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
                    "email": form.cleaned_data["email"],
                    "phonenumber": form.cleaned_data["phone_number"],
                    "txRef": txRef,
                    "enckey": encKey,
                    "userid": str(user.id),
                }
                order_details = {
                    "full_name": form.cleaned_data["firstname"]
                    + " "
                    + form.cleaned_data["lastname"],
                    "address1": form.cleaned_data["address1"],
                    "address2": form.cleaned_data["address2"],
                    "city": form.cleaned_data["city"],
                    "phone": form.cleaned_data["phone_number"],
                    "post_code": form.cleaned_data["zipcode"],
                    "order_key": txRef,
                    "userid": str(user.id),
                    "cardno": str(form.cleaned_data["cardno"])[-4:],
                    "amount": basket.get_total_price(),
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
                for item in product_list2(request)["product_list2"]:
                    product = item[0]
                    product.count = product.count - item[1]
                    product.save()
                basket.clear()
                return render(request, "payment/orderplaced.html")
            else:
                del request.session["payload"]
                return render(
                    request,
                    "payment/payment_form.html",
                    {"form": form, "errMsg": True},
                )

        except (
            RaveExceptions.CardChargeError,
            RaveExceptions.TransactionVerificationError,
            RaveExceptions.TransactionValidationError,
        ) as e:
            del request.session["payload"]
            form = PaymentForm()
            return render(
                request,
                "payment/payment_form.html",
                {"form": form, "errMsg": True},
            )


# def orderplaced(request):
#    basket = Basket(request)
#    for item in product_list2(request)['product_list2']:
#        product = item[0]
#        product.count = product.count - item[1]
#        product.save()
#    basket.clear()
#    return render(request, 'payment/orderplaced.html')
