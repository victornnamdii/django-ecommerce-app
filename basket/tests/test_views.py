from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product
from accounts.models import UserBase


User = UserBase


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(email='test@test.com')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django intermediate', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django advanced', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        self.client.post(
            reverse('basket:basket_add'), {"product_id": 1, "product_qty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"product_id": 2, "product_qty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {"product_id": 3, "product_qty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"product_id": 2, "product_qty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 5})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"product_id": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': 20.0, 'total': 31.5})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"product_id": 2, "product_qty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': 40.0, 'item_total_price': 31.5, 'total': 51.5})
