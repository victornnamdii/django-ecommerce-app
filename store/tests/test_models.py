from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from store.models import Category, Product
from accounts.models import UserBase


User = UserBase


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category data entry
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_return(self):
        """
        Test Category data return
        """
        data = self.data1
        self.assertEqual(str(data), 'django')


class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(email='test@test.com')
        self.data1 = Product(category_id=1, created_by_id=1,
                             title='product name',
                             slug='product-name',
                             price=20.00,
                             image='django', count=0)

    def test_product_model_entry(self):
        """
        Test Product data entry
        """
        data = self.data1
        data.save()
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'product name')
        self.assertFalse(data.in_stock)
        data.count = 25
        data.save()
        self.assertTrue(data.in_stock)
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/product-name')
