from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class DeliveryOptions(models.Model):
    """
    Table for Delivery Options
    """

    DELIVERY_CHOICES = [
        ("PU", "Pick Up"),
        ("HD", "Home Delivery"),
        ("ID", "International Delivery"),
    ]

    delivery_name = models.CharField(
        _("delivery name"), max_length=255, help_text=_("Required")
    )

    delivery_price = models.DecimalField(
        _("delivery price"),
        max_digits=12,
        decimal_places=2,
        help_text=_("Maximum 9999999999.99"),
        error_messages={
            "name": {
                "max_length": _("price must be between 0 and 9999999999.99")
            }
        },
    )

    delivery_method = models.CharField(
        _("delivery method"),
        max_length=255,
        choices=DELIVERY_CHOICES,
        help_text=_("Required"),
    )

    delivery_timeframe = models.CharField(
        _("Delivery timeframe"), max_length=255, help_text=_("Required")
    )

    delivery_window = models.CharField(
        _("Delivery window"), max_length=255, help_text=_("Required")
    )

    order = models.IntegerField(
        verbose_name=_("list_order"), help_text=_("Required"), default=0
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self) -> str:
        return self.delivery_name


class PaymentSelections(models.Model):
    """
    Store Payment options
    """

    name = models.CharField(_("Name"), max_length=255, help_text=_("Required"))

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self) -> str:
        return self.name
