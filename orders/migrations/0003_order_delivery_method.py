# Generated by Django 4.1.4 on 2023-04-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_rename_post_code_order_postal_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_method",
            field=models.CharField(default="Standard Delivery", max_length=100),
            preserve_default=False,
        ),
    ]