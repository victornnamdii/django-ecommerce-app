# Generated by Django 4.1.4 on 2023-04-21 20:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_product_users_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                editable=False,
                max_digits=12,
                verbose_name="Active Price",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="use_discount",
            field=models.BooleanField(
                default=False, verbose_name="Use discount price?"
            ),
        ),
    ]
