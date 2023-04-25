# Generated by Django 4.1.4 on 2023-04-25 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0004_remove_address_town_city_address_city_address_state",
        ),
        ("orders", "0004_order_order_shipped"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="address1",
        ),
        migrations.RemoveField(
            model_name="order",
            name="address2",
        ),
        migrations.RemoveField(
            model_name="order",
            name="city",
        ),
        migrations.RemoveField(
            model_name="order",
            name="country_code",
        ),
        migrations.RemoveField(
            model_name="order",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="order",
            name="postal_code",
        ),
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="accounts.address",
                verbose_name="Shipping Address",
            ),
        ),
    ]
