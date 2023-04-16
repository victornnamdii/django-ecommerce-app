from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,
                     self).get_queryset().filter(is_active=True)


class Category(models.Model):
    """Categories of the items"""
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products"""
    category = models.ForeignKey(Category, related_name='product',
                                 on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='product_creator',
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1, null=False)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.in_stock = self.count > 0
        super().save()
