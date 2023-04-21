# Generated by Django 4.1.4 on 2023-04-21 20:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0003_product_price_product_use_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="users_wishlist",
            field=models.ManyToManyField(
                editable=False,
                related_name="user_wishlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]