from django.core.exceptions import PermissionDenied
from basket.basket import Basket


def cart_required(function):
    def wrap(request, *args, **kwargs):
        basket = Basket(request)
        if len(basket) > 0:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
