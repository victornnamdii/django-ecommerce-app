from .basket import Basket
from store.models import Product
from django.conf import settings


def basket(request):
    return {'basket': Basket(request)}


def product_list2(request):
    prod_list = []
    basket = request.session[settings.BASKET_SESSION_ID]
    for item in basket.keys():
        product = Product.objects.get(id=item)
        prod_list.append([product, basket[item]['qty']])
    return {'product_list2': prod_list}
