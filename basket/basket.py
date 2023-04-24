from decimal import Decimal

from django.conf import settings

from checkout.models import DeliveryOptions
from store.models import Product


class Basket:
    """
    Base basket class
    """

    def __init__(self, request):
        self.session = request.session
        self.basket = self.session.get(settings.BASKET_SESSION_ID, False)
        if not self.basket:
            self.basket = self.session[settings.BASKET_SESSION_ID] = {}
        # self.session = request.session
        # basket = self.session.get('skey')
        # if 'skey' not in self.session:
        # basket = self.session['skey'] = {}
        # self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating the user's basket session data
        """
        product_id = str(product.id)

        if product_id not in self.basket.keys():
            self.basket[product_id] = {
                "price": float(product.price),
                "qty": int(product_qty),
            }
        else:
            self.basket[product_id]["qty"] += int(product_qty)

        self.save()

    def update(self, product, product_qty):
        """
        Updating the user's basket session data
        """
        product_id = str(product)

        if product_id in self.basket.keys():
            self.basket[product_id]["qty"] = product_qty

        self.save()

    def __len__(self):
        """
        Get basket data and count total items
        """
        # count = 0
        # for item in self.basket.values():
        #   count += item['qty']
        # return count
        return sum(item["qty"] for item in self.basket.values())

    def __iter__(self):
        """
        Making basket iterable (with all the product ids)
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def get_subtotal_price(self):
        """
        Return basket total price
        """
        return sum(
            item["qty"] * item["price"] for item in self.basket.values()
        )

    def get_total_price(self):
        """
        Return basket total price
        """
        shipping = Decimal(0.00)

        subtotal = sum(
            item["qty"] * Decimal(item["price"])
            for item in self.basket.values()
        )
        if "purchase" in self.session:
            shipping = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]
            ).delivery_price

        return float(round(subtotal + shipping, 2))

    def get_delivery_price(self):
        shipping = 0.00

        if "purchase" in self.session:
            shipping = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]
            ).delivery_price

        return shipping

    def delete(self, product_id):
        """
        Deletes an item from the basket
        """
        id = str(product_id)
        if id in self.basket:
            del self.basket[id]

        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session["address"]
        del self.session["purchase"]
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(
            item["qty"] * Decimal(item["price"])
            for item in self.basket.values()
        )
        total = subtotal + deliveryprice
        return round(total, 2)
