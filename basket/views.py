from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket
from store.models import Product

# Create your views here.


def basket_summary(request):
    return render(request, 'basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_qty=product_qty)
        response = JsonResponse({'qty': len(basket)})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product_id)
        response = JsonResponse({'qty': len(basket),
                                 'subtotal': basket.get_subtotal_price(),
                                 'total': basket.get_total_price()})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product=product_id, product_qty=product_qty)
        basket_qty = len(basket)
        basket_subtotal_price = basket.get_subtotal_price()
        item = basket.basket[str(product_id)]
        item_total_price = round((item['qty'] * item['price']) + 11.50, 2)
        response = JsonResponse({'qty': basket_qty,
                                 'subtotal': basket_subtotal_price,
                                 'item_total_price': item_total_price,
                                 'total': basket.get_total_price()})
        return response
