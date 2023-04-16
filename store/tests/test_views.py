from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.conf import settings
from accounts.models import UserBase

from store.models import Category, Product
from store.views import all_products
from importlib import import_module


User = UserBase


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(email='test@test.com')
        Product.objects.create(category_id=1, created_by_id=1,
                               title='product name',
                               slug='product-name',
                               price=20.00, image='django',
                               count=9)

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_url(self):
        """
        Test Product urls
        """
        response = self.c.get(reverse('store:product_detail',
                                      args=['product-name']))
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """
        Test Category urls
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test homepage contents
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('Electronic Store', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_url_allowed_hosts2(self):
        """
        Testing allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='oboy.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)
