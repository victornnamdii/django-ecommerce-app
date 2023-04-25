from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from basket.basket import Basket


def cart_required(function):
    def wrap(request, *args, **kwargs):
        basket = Basket(request)
        if len(basket) > 0:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("basket:basket_summary"))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def delivery_required(function):
    def wrap(request, *args, **kwargs):
        if "purchase" in request.session:
            return function(request, *args, **kwargs)
        else:
            messages.success(request, "Please select delivery address")
            return HttpResponseRedirect(reverse("checkout:deliverychoices"))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def address_required(function):
    def wrap(request, *args, **kwargs):
        if "address" in request.session:
            return function(request, *args, **kwargs)
        else:
            messages.success(request, "Please select delivery address")
            return HttpResponseRedirect(reverse("checkout:delivery_address"))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def billing_required(function):
    def wrap(request, *args, **kwargs):
        address = request.session.get("address")
        if address and "billing" in address:
            return function(request, *args, **kwargs)
        else:
            messages.success(request, "Please select billing address")
            return HttpResponseRedirect(reverse("checkout:billing_address"))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
