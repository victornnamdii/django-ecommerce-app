# Generated by Django 4.1.4 on 2023-04-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_order_delivery_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_shipped",
            field=models.BooleanField(
                default=False, verbose_name="Order processed/shipped?"
            ),
        ),
    ]